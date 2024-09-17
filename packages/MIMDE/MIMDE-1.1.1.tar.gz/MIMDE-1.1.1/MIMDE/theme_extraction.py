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
import tiktoken
from pydantic_classes import LowLevelResponseAnalysis, RoughHighLevelAnalysis, HighLevelResponseAnalysis
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')
import re
import yaml
import sys

## imports within the package
from .cost import calculate_chunks_theme_extraction

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
