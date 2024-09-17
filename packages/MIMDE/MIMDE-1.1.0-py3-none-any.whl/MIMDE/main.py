import yaml
import argparse
import os
import pandas as pd

## Local Imports
from .data_cleaner import read_input_data, theme_to_text
from .LLM_toolkit import create_llm
from .theme_extraction import identify_themes
from .response_mapping import map_responses_to_themes

def Brute_force_pipeline(config_path: str):   
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    demo = dict(config['GENERAL']['DEMO'])
    consultation_name = config['GENERAL']['consultation_name']
    model_name = config['BRUTE_FORCE']['MODEL']

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
    output_path = os.path.join('data', f'{consultation_name}/output/Brute_force_analysis_{model_name}.xlsx')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = pd.ExcelWriter(output_path)
    model = create_llm(model_name)

    # Iterate over the dataframes and extract insights for each question
    dataframes_annotated = {}
    total_cost = 0
    for key, df in consultation_data.items():
        current_question = s_q_map_dict[key]
        print(f"Analyzing {key}")
        themes,cost_themes = identify_themes(df, model, question_string=current_question, prompt_instruction=prompt_instruction)
        mapped_responses,cost_reponses = map_responses_to_themes(df, themes, current_question, model)
        clean_responses = theme_to_text(themes, mapped_responses)
        clean_responses.to_excel(writer, sheet_name= key, index=False)
        total_cost += cost_themes + cost_reponses
        dataframes_annotated[key] = themes
    print(f"Total cost of Analysis: {total_cost}")
    writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="")
    args = parser.parse_args()
    if args.config=="":
        raise ValueError('Please provide a path to your config file using python Brute_force.py --config your_config_file_path')
    Brute_force_pipeline(args.config)
    print("Brute force pipeline completed successfully for consultation: ")
