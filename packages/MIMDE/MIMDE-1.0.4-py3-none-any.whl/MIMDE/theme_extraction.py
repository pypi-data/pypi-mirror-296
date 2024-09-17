import pandas as pd
from typing import Dict, Tuple
from sklearn.cluster import KMeans
import json
from litellm import embedding
from output_summaries import generate_written_summaries
from datetime import datetime
from copy import deepcopy
from .LLM_toolkit import create_llm
from pydantic import ValidationError
from typing import Dict
from pydantic import BaseModel, validator
from typing import List
from transformers import GPT2Tokenizer
import os
import tiktoken
from pydantic_classes import LowLevelResponseAnalysis, RoughHighLevelAnalysis, HighLevelResponseAnalysis
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')
#tokenizer = T5Tokenizer.from_pretrained("t5-small")
import re
from .data_cleaner import read_input_data
from cost import calculate_chunks_theme_extraction
class LowLevelTheme(BaseModel):
    theme: str

class LowLevelResponseAnalysis(BaseModel):
    themes: List[LowLevelTheme]


def json_format(llm_response, PydanticClass):
    """
    Attempts to generate a valid final themes JSON response using the specified model.
    
    Notee: This function is called by 'identify_themes'.
    """
    # Attempt to generate a valid final themes JSON
    for attempt in range(5):
        try:
            llm_response = json.loads(llm_response)
            error = None
            return llm_response['themes']
        except (json.decoder.JSONDecodeError, ValueError, ValidationError) as e:
            if attempt < 4:
                print(f"Attempt {attempt+1} to generate a valid final themes JSON failed due to a {e}, retrying...")
                continue
            else:
                if PydanticClass==LowLevelResponseAnalysis:
                    print(f"Attempt {attempt+1} to generate a valid final themes JSON failed due to a {e}, retrying...")
                    print("Using default error schema for LowLevelResponseAnalysis...")
                    # Default error schema for LowLevelResponseAnalysis
                    default_error_schema = {
                        "themes": [{"theme": "Error: Unable to generate valid themes"}],
                        "mcq_contradiction": False,
                        "outlier": {
                            "is_outlier": False,
                            "outlier_category": {
                                "irrelevant": False,
                                "incoherent": False,
                                "extreme": False,
                                "other": False
                            },
                            "outlier_reason": None,
                            "outlier_score": 0.0
                        }
                    }
                    llm_response = PydanticClass(**default_error_schema)
                    return llm_response
                else:
                    print(f"Attempt {attempt+1} to generate a valid final themes JSON failed due to a {e}, please check the prompt and try again.")
                    raise
def ask_llm(model, user_prompt):
    # Attempt to generate a valid final themes JSON  - work on this a little more later
    if ('gpt-4' in model.model):
       llm_response = model.run(user_prompt = user_prompt, response_format={"type": "json_object"}) 
       return json_format(llm_response, LowLevelResponseAnalysis)
    else:
        for attempt in range(5):
            llm_response = model.run(user_prompt = user_prompt)
            try:
                themes_string = llm_response.split("[")[1].split("]")[0]
                themes_list = re.split(r'\s*,\s*', themes_string)
                return themes_list
            except:
                print(f"unable to extract themes in attempt {attempt+1}\nllm response: {llm_response}")
                continue
        return []

def identify_themes(df: pd.DataFrame, model, question_string:str, prompt_instruction:str = "") -> Tuple[pd.DataFrame, pd.DataFrame]:

    themes_df = pd.DataFrame()
    choices = df['mcq_response'].unique()
    total_cost = 0
    for choice in choices:
        responses = df.loc[df['mcq_response'] == choice, 'response']
        prompt_input = f"""Please analyze the following survey responses:
            Question: {question_string}
            "Multiple Choice Selection: " {choice}
            Open-ended Responses: """
        chunk_indices, cost = calculate_chunks_theme_extraction(responses, prompt_input+prompt_instruction, model)
        total_cost += cost
        num_chunks = len(chunk_indices)-1
        print(f"Extracting themes for: {choice} with number of chunks: {num_chunks} and number of responses: {len(responses)}")
        llm_response_list = []
        for index in range(len(chunk_indices)-1): 
            response_chunk = responses[chunk_indices[index]:chunk_indices[index+1]] 
            responses_string = ""
            for i, response in enumerate(response_chunk):
                responses_string =  responses_string + str((i+1)) + "." + response + "\n" 
            prompt = prompt_input + responses_string + prompt_instruction
            print(f"analyzying chunk {index} with len {len(tokenizer.encode(prompt))} and number of responses: {len(response_chunk)}")
            llm_response = ask_llm(model, prompt)
            llm_response_list = llm_response_list + llm_response
        if num_chunks > 1:
            prompt =  f""" please analyze the following survey themes found and extract the main themes from the list provided.
            Question: {question_string}
            "Multiple Choice Selection: " {choice}
            Themes: {llm_response_list}""" + prompt_instruction.split("4.")[0] + "Output: Provide the theme(s)in the specified list {{'themes':[ str, str, ..., str], }}"
            print(f"analyzing all chunks with len {len(tokenizer.encode(prompt))}") 
            llm_response = ask_llm(model, prompt)
        themes = {}        
        for i, theme in enumerate(llm_response):
            themes[f'themes{i+1}'] = theme
        themes['number_of_responses'] = len(responses)
        themes['choice'] = choice
        themes_dict = pd.DataFrame([themes])
        themes_df = pd.concat([themes_df, themes_dict], axis=0)
        print(f"Analyzing responses for: {choice}") 
    return themes_df, total_cost

def themes_Brute_force_pipeline(demo, consultation_name, model_name, prompt_instruction:str = ""): 
    prompt_instruction = """Instructions: 
        1. Identify the main theme(s) in the open-ended provided responses that explain the respondents' multiple choice selection. 
        2. Provide detailed identified theme(s) without using qualitative descriptors (e.g., 'good', 'poor'). 
        3. Do not output any explanatory comments such as: 'Here are the main themes...'. 
        4. provide a theme if and only if it is mentioned by at least '5%' of the responses. 
        5. Try to be concise and avoid redundancy. """
    list_output_format =  """ Output: Provide the theme(s)in the specified list {{'themes':[ str, str, ..., str], }}"""
    json_output_format = """Output: Provide the theme(s)in the specified json schema: {{ "themes": [str, strs, ..., str]}}"""
    if 'gpt-4' in model_name:
        prompt_instruction = prompt_instruction + json_output_format
    elif 'llama' in model_name:
        prompt_instruction = prompt_instruction.split("5.")[0] + json_output_format
    else:
        prompt_instruction = prompt_instruction + list_output_format

    consultation_data, themes, s_q_map_dict = read_input_data(consultation_name, model_name, demo, 'theme_extraction')
    output_path = os.path.join('data', f'{consultation_name}/output/insight_{model_name}.xlsx')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    themes_writer = pd.ExcelWriter(output_path)
    model = create_llm(model_name)

    # Iterate over the dataframes and extract insights for each question
    dataframes_annotated = {}
    total_cost = 0
    for key, df in consultation_data.items():
        current_question = s_q_map_dict[key]
        print(f"Analyzing {key}")
        themes,cost = identify_themes(df, model, question_string=current_question, prompt_instruction=prompt_instruction)
        total_cost += cost
        dataframes_annotated[key] = themes
        themes.to_excel(themes_writer, sheet_name=key, index=False)
    print(f"Total cost for theme extraction: {total_cost}")
    themes_writer.close()
