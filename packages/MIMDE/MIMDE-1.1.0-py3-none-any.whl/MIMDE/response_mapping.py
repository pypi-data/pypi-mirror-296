import pandas as pd
from typing import Dict, Tuple
from sklearn.cluster import KMeans
import json
from litellm import embedding
from output_summaries import generate_written_summaries
from datetime import datetime
from copy import deepcopy
from pydantic import ValidationError
from typing import Dict
from pydantic import BaseModel, validator
from typing import List
from transformers import GPT2Tokenizer
import os
import re
import tiktoken
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')

from .cost import calculate_chunks_response_mapping

class LowLevelTheme(BaseModel):
    theme: str

class LowLevelResponseAnalysis(BaseModel):
    themes: List[LowLevelTheme]

def map_response_chunks(model, prompt):
    mapping_df = pd.DataFrame(columns= ['response','theme(s)'])
    if ('gpt-4' in model.model):
        llm_response = model.run(user_prompt = prompt , response_format={"type": "json_object"})
        llm_response = json.loads(llm_response)
        for mapped_response in llm_response['mapped_responses']:
            mapping_df = pd.concat([mapping_df, pd.DataFrame([mapped_response])], axis=0)
        return mapping_df
    else:
        llm_response = model.run(user_prompt = prompt)
        llm_response = llm_response.split("mapped_responses")[1]
        mapped_responses = re.split(r'{*},', llm_response)
        for i, mapped_response in enumerate(mapped_responses):
            if "theme(s)" in mapped_response and "response_id" in mapped_response:
                themes = mapped_response.split('theme(s)')[1].split("[")[1].split("]")[0]
                response_id = int(re.findall(r'\d+', mapped_response.split('"response_id"')[1])[0])
                mapping_df = pd.concat([mapping_df, pd.DataFrame([{'response_id': response_id, 'theme(s)': themes}])], axis=0)
        return mapping_df
    
def map_responses_to_themes(df: pd.DataFrame, themes, question_string, model) -> pd.DataFrame:
    prompt_instruction = """
    You have identified the main themes in the open-ended provided responses that explain the respondents'
    multiple choice selection. 
    Please assign each response to one or more themes from the list of themes provided. 
    Instructions:
    1. Do not output any explanatory comments such as: "Here are the themes assigned...".
    2. Do not add any additional themes to the list provided and just pick one or more from the list.
    3. Assign a row to each response with the theme(s) mapped to it according to the output example.
    4. If a response does not fit any of the themes provided, leave the cell blank.
    5. Output: Provide the result in the specified json schema: 
    {"mapped_responses": [
    {"theme(s)": [theme_id, theme_id,...,theme_id], "response_id": id},
    {"theme(s)": [theme_id, theme_id,...,theme_id], "response_id": id},
    ...
    {"theme(s)": [theme_id, theme_id,...,theme_id], "response_id": id}
    ]}"""
    choices = df['mcq_response'].unique()
    df['response_id'] = df.index
    df['theme(s)'] = None
    theme_columns = [theme_column for theme_column in themes.columns if 'theme' in theme_column]
    for choice in choices:
        responses = df.loc[df['mcq_response'] == choice, 'response']
        ids = df.index[df['mcq_response'] == choice].tolist()
        prompt_question = f"""Please analyze the following survey responses and map responses to the themes:
        Question: {question_string}
        {"Multiple Choice Selection: " + choice}"""
        choice_themes = themes.loc[themes['choice'] == choice, [theme_column for theme_column in theme_columns]].values.tolist()[0]
        themes_string = ""
        for i,theme in enumerate(choice_themes):
            if theme != None:
                themes_string =  themes_string + f'theme_{i+1}: {theme}\n'
        chunk_indices, cost = calculate_chunks_response_mapping(responses, choice_themes, prompt_question + prompt_instruction, model)
        num_chunks = len(chunk_indices)-1
        print(f"mapping responses for : {choice} with number of chunks: {num_chunks} and number of responses: {len(responses)}")
        for index in range(len(chunk_indices)-1): 
            response_chunk = responses[chunk_indices[index]:chunk_indices[index+1]] 
            id_chunks = ids[chunk_indices[index]:chunk_indices[index+1]]
            response_string = ""
            for i,response in enumerate(response_chunk):
                response_string =  response_string + f'response_id: {id_chunks[i]}, response_text: {response}\n'
            prompt_input = f"""Open-ended Responses: {response_string} 
            themes : {themes_string} """
            prompt = prompt_question + prompt_input + prompt_instruction
            print(f"analyzing chunk {index} with len {len(tokenizer.encode(prompt))} and number of responses: {len(response_chunk)}")
            llm_response = map_response_chunks(model, prompt)
            print('llm responded')
            df = df.merge(llm_response[['response_id','theme(s)']], on='response_id', how='left')
            df['theme(s)'] = df['theme(s)_x'].combine_first(df['theme(s)_y'])
            df.drop(columns=['theme(s)_x', 'theme(s)_y'], inplace=True)
    df.drop(columns=['response_id'], inplace=True)
    return df, cost

