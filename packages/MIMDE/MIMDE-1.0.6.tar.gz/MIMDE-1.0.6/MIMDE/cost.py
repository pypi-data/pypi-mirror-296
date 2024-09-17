# Import basic necessary packages
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from timeit import default_timer as timer
from transformers import LlamaTokenizer
from transformers import GPT2Tokenizer
from transformers import T5Tokenizer
tokenizer = GPT2Tokenizer. from_pretrained("gpt2") ### select tokenizer
import tiktoken
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')

def calculate_chunks_theme_extraction(responses, system_prompt, model):
    context_length = model.context_length
    per_token_input_cost = model.input_cost
    per_token_output_cost = model.output_cost
    if (system_prompt == ""):
        system_prompt = """Instructions: 
        1. Identify the main theme(s) in the open-ended provided responses that explain the respondents' multiple choice selection. 
        2. Provide detailed identified theme(s) without using qualitative descriptors (e.g., 'good', 'poor'). 
        3. Do not output any explanatory comments such as: 'Here are the main themes...'. 
        4. provide a theme if and only if it is mentioned by at least '5%' of the responses. 
        5. Try to be concise and avoid redundancy. """
    chunk_indices = [0]
    responses_string = ""
    index_response = 0
    free_space = 20
    number_themes =   10
    len_theme = 20
    len_output =  number_themes*len_theme + free_space
    len_instruction = len(tokenizer.encode(system_prompt))
    cost = 0
    for index, response in enumerate(responses):
        responses_string =  responses_string + str((index_response+1)) + "." + response + "\n" 
        len_responses = len(tokenizer.encode(responses_string))
        if (len_responses + len_instruction + len_output) >= context_length:
            chunk_indices.append(index)
            index_response = 0
            responses_string = str((index_response+1)) + "." + response + "\n"
            cost+= (len_responses + len_instruction)*per_token_input_cost/1000 + len_output*per_token_output_cost/1000       
    if chunk_indices[-1] != len(responses):
        chunk_indices.append(len(responses))
        cost+= (len_responses + len_instruction)*per_token_input_cost/1000 + len_output*per_token_output_cost/1000
    return (chunk_indices, cost)

def calculate_chunks_response_mapping(responses, themes, system_prompt, model):

    context_length = model.context_length
    per_token_input_cost = model.input_cost
    per_token_output_cost = model.output_cost
    if (system_prompt == ""):
        system_prompt = """
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
    themes_string = ",".join([str(id) + '. ' + str(theme) + '\n' for id, theme in enumerate(themes)])
    len_mapped_responses_format = len(tokenizer.encode("""{"theme(s)":[], "response_id": id}""")) + len(tokenizer.encode("theme_id,")) * len(themes)
    len_prefix_response = len(tokenizer.encode("""{"mapped_response":[]}"""))
    chunk_indices = [0]
    responses_string = ""
    index_response = 0
    cost = 0
    len_instruction = len(tokenizer.encode(system_prompt)) + len(tokenizer.encode("responses: , themes:")) + len(tokenizer.encode(themes_string))
    for index, response in enumerate(responses):
        responses_string =  responses_string + str((index_response+1)) + "." + response + "\n" 
        len_output = len_mapped_responses_format*(index_response+1) + len_prefix_response
        len_responses = len(tokenizer.encode(responses_string))
        if (len_responses + len_instruction + len_output) >= context_length:
            chunk_indices.append(index)
            index_response = 0
            responses_string = str((index_response+1)) + "." + response + "\n"  
            cost+= (len_responses + len_instruction)*per_token_input_cost/1000 + len_output*per_token_output_cost/1000     
    if chunk_indices[-1] != len(responses):
        chunk_indices.append(len(responses))
        cost+= (len_responses + len_instruction)*per_token_input_cost/1000 + len_output*per_token_output_cost/1000
    return (chunk_indices, cost)
