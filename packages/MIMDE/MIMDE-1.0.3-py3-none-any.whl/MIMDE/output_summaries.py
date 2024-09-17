import pandas as pd
import numpy as np
import json
import subprocess
from LLM_toolkit import create_llm
import argparse
import os
import ast
import yaml
import re

# Ideally this should be a function that gets run (or is called directly) after the high level pipeline function

# By question, the input is question text, extracted insights, and representative responses (embeddings?)

# Save the output to a J-SON file that can be incorporated into an R markdown template which is called at the end
# Can discuss this bit, but this would allow us to use the package Harry shared 


def load_summary_info(input_path,s_q_map_path):
    """
    Load in the summary data, return all the information in dictionaries with question vairbales as the keys.

    Parameters:
    - input_path (str, optional): Path to the output file in the high level pipeline.

    Returns:
    - thematically_coded_dict: A dictionary (keys are the quesitons) of themetically coded response data, values are the dataframe outputs from the high level pipeline.
    - insight_dict: A dictionary (keys are the quesitons) of extracted insights, values are the dataframe outputs from the high level pipeline.
    """
    # get the thematically coded responses (one sheet per dict)
    thematically_coded_dict = pd.read_excel(input_path, sheet_name=None)

    # get the cluster summaries file_name
    file_name = input_path.replace(".xlsx", "_cluster_summaries.xlsx")
    # read in all the sheets to a dictionary (one sheet per dict)
    insight_dict = pd.read_excel(file_name, sheet_name=None)

    # read in all the questions, convert to a dict
    question_text = pd.read_excel(s_q_map_path)
    question_dict = question_text.set_index('question_column_names')['machine_readable_question_text'].to_dict()

    return {"thematically_coded_dict":thematically_coded_dict, 
            "insight_dict":insight_dict, 
            "question_dict":question_dict}

def save_written_summaries(written_summary_dict,
                           input_path):
    """
    Saves the generated summary information to JSON.

    Parameters:
    - written_summary_dict (dict): The LLM generated summary dict.
    - input_path (str): Path to the folder where the output should be stored.

    Returns:
    - None: Save the summary information in json format.
    """

    file_name = input_path.replace(".xlsx", "_llm_summaries.json")

    with open(file_name, 'w') as f:
        json.dump(written_summary_dict, f)


def create_written_summaries(model,
                             insight,
                             thematically_coded_dict,
                             question_text,
                             col):
    """
    Orchestrates the process of analyzing high-level data using configurations specified in an INI file.

    Parameters:
    - model: An LLM object that can be used to generate summaries.
    - insight (str): The insight to be summarised.
    - thematically_coded_dict (df): A dataframe of the responses for the question this insight is derived from.
    - question_text (str): The question text of the insight.
    - col (str, optional): The column name the insight is coming from (should have the MCQ value if applicable)

    Returns:
    - Dictionary: A dictionary containing all the information need to produce a summary of the provided template.
    """

    mcq_response = False # keep this false for now as we figure out the best way to incorporate multiple choice selections

    # filter to rows to responses containg the theme
    try:
        insight_df =  thematically_coded_dict[thematically_coded_dict["extracted_insights_aggregate"].str.contains(insight)]
    except TypeError:
        print(f"Issue with Insight: {insight}; returning an empty string")
        return ""
    
    # If the insight is from an mcq it is in a different column...
    if len(insight_df)==0:
        insight_df =  thematically_coded_dict[thematically_coded_dict["extracted_insights_by_mcq"].str.contains(insight)]
        mcq_response = True
        print("using the MCQ column")

    num_supporters = len(insight_df)
    representative_responses = insight_df.sample((5 if len(insight_df)>5 else len(insight_df)))["response"].tolist()

    
    join_character = "\n"
    user_prompt = f"""
    The insight "{insight}" was extracted through a thematic analysis of the question: "{question_text}".
    In a short pargraph, your task is to summarise the reasoning behind this extracted insight drawing on the context of the representative responses provided below. 
    {f'For additional context, keep in mind that this insight is from the subset of respondents which selected "{col}" on a related multiple choice question. ' if mcq_response else ""}
    1. Respond as succinctly as possible, while providing enough information to give a policy analyst a good understanding of the extracted insight.
    2. Do not directly quote any of the representative responses or make up information that does not follow logically from the representative responses. 
    3. Do not include any explanatory statements such as "The summary of this insight is" or "Given the context of the representative responses". 
    4. Provide only the short summary paragraph as free text, without additional explanatory information after the summary is returned. 
    5. Ensure the summary sticks to only explaining the reasoning behind the extracted insight "{insight}" without straying into other topic areas.
    6. If you are unable to generate a summary due to a lack of context, please respond with "Not enough information to summarise this insight". 
    Representative responses which mentioned this extracted insight:
    {join_character.join(["R"+str(a+1)+": "+b for a,b in enumerate(representative_responses)])}
    """

    # Generate summary for the current cluster using the language model
    llm_summary = model.run(user_prompt)

    return {"short_summary":llm_summary,
            "num_supporters":num_supporters,
            "representative_responses":representative_responses}


def create_final_templates(input_path,consultation_name,rscript_location):
    """
    Executes R code to generate all of the summary output files.

    Parameters:
    - input_path (str, optional): Path to the folder where the output should be stored.

    Returns:
    - None: Executes R code to generate all of the summary output files.
    """
    json_file = input_path.replace(".xlsx", "_llm_summaries.json")
    output_directory = os.path.dirname(input_path)

    subprocess.call([rscript_location,'src/create_prompt_templates.R', json_file, output_directory,consultation_name])




def generate_written_summaries(config_path):
    """
    Orchestrates the process of generating written summaries, after the high level pipeline is run.

    Parameters:
    - directory_path (str, optional): Path to the directory where the pipeline output is saved.
    - model (str, optional): An LLM-factory object that can be used to generate summaries.

    Returns:
    - None: Executes the full pipeline from reading in data, extracting insights, and saving results.
    """
    # First load in and organize the data that we will need
    
    with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    
    consultation_name = config['GENERAL']['consultation_name']
    output_dtm_str = config['LOW_LEVEL']['FILES']['output_datetime']
    
    input_path = os.path.join('data', consultation_name, 'output', output_dtm_str, 'high_level_analysis_output.xlsx')
    s_q_map_path = os.path.join('data', consultation_name, 'input', config['GENERAL']['sheet_question_mapping_file'])
    rscript_location = config['R']['rscript_location']
    model = create_llm(**dict(config['HIGH_LEVEL']['MODEL']))

    
    
    print('Loading summary info...')
    summary_info = load_summary_info(input_path,
                                     s_q_map_path)
    

    # Use a LLM to generate the written summaries
    print("Creating written summaries...")
    written_summary_dict = {}
    for question in summary_info["insight_dict"]: # iterate over questions
        print(f"For question: {question} which has {len( [a for a in list(summary_info['insight_dict'][question].columns) if 'responses' not in a])} question columns...")
        question_mcq_summary_dict = {}
        for col in [a for a in list(summary_info["insight_dict"][question].columns) if "responses" not in a]: # iterate over insight columns (aggregate + any others)
            question_summary_dict = {}
            for insight in summary_info["insight_dict"][question][col].tolist():
                temp_summary_dict = create_written_summaries(model,
                                                             insight,
                                                             summary_info["thematically_coded_dict"][question],
                                                             summary_info["question_dict"][question],
                                                             col)
                if temp_summary_dict=="":
                    continue
                # add in the top n responses
                top_n_responses = summary_info["insight_dict"][question].loc[summary_info["insight_dict"][question][col] == insight, col+"_repr_responses"].iloc[0]
                # Having trouble with this formatting, converting a list
                top_n_responses = ast.literal_eval(top_n_responses)
                temp_summary_dict["top_n_responses"] = [a['response'] for a in top_n_responses]
                temp_summary_dict["top_n_low_level_themes"] = [a['low_level_themes_used'] for a in top_n_responses]
                question_summary_dict[insight] = temp_summary_dict
            
            question_mcq_summary_dict[col]=question_summary_dict
        written_summary_dict[question]={"question_text":summary_info["question_dict"][question],
                                        "summary_dict":question_mcq_summary_dict,
                                        "total_responses":len(summary_info["thematically_coded_dict"][question])}


    # Save the output to a J-SON file that can be incorporated into an R markdown template
    print("Saving written summaries...")
    save_written_summaries(written_summary_dict,
                           input_path)

    # Create final templates (call the R code)
    print("Creating creating the final written output documents...")
    create_final_templates(input_path,consultation_name,rscript_location)
    print("Output file created sucessfully.")