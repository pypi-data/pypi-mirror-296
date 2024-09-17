import os
from typing import List, Dict, Any
import requests
import time
from litellm import completion, InternalServerError
from dotenv import load_dotenv
import yaml  # Add this import
import json

class LLM_Base:
    """
    Abstract base class for different LLM types.
    """
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def run(self, user_prompt:str, system_prompt:str="You are a helpful assistant.", **kwargs: Any) -> str:
        messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                    ]
        max_retries = 12
        for attempt in range(max_retries):
            try:
                if 'gpt' in self.model:
                    return self._completion(messages, **kwargs)
                else:
                    llm_inputs = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    **kwargs
                    }
                    self.headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                    }
                    response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(llm_inputs))
                    return response.json()['choices'][0]['message']['content']
            except (requests.ConnectionError, KeyError, AttributeError, InternalServerError) as e:
                if attempt < max_retries - 1:
                    print(f"{e}, retrying...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                    continue
                else:
                    raise  # Re-raise the last exception if all retries fail

    def _completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        raise NotImplementedError("Subclass must implement this method")


class LITELLM(LLM_Base):
    def __init__(self,model_config):
        super().__init__(model_config['model'], model_config['api_key'])
        self.api_type = "litellm"
        self.context_length = model_config['context_length']

    def _completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        chat_completion = completion(
            model=self.model,
            api_key=self.api_key,
            messages=messages,
            **kwargs
        )
        return chat_completion['choices'][0]['message']['content']


class LITELLM_AZURE(LLM_Base):
    def __init__(self, model_config):
        super().__init__(model_config['model'], model_config['api_key'])
        self.api_version = model_config['api_version']
        self.endpoint = model_config['endpoint']
        self.api_type = "azure"
        self.context_length = model_config['context_length']
        self.input_cost = model_config['input_cost']
        self.output_cost = model_config ['output_cost']

    def _completion(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        chat_completion = completion(
            model=f"azure/{self.model}",
            api_base=self.endpoint,
            api_version=self.api_version,
            api_key=self.api_key,
            messages=messages,
            **kwargs
        )
        return chat_completion['choices'][0]['message']['content']


def get_model_config(model_name: str) -> Dict[str, str]:
    model_configs_path = os.path.join('MIMDE', 'config', 'model_configs.yaml')
    with open(model_configs_path, 'r') as file:
        configs = yaml.safe_load(file)
    
    if model_name not in configs['LLMs']:
        raise ValueError(f"Unknown model: {model_name}")
    
    return configs['LLMs'][model_name]

def create_llm(model_name: str) -> LLM_Base:
    model_config = get_model_config(model_name)
    if model_config['api_type'] == 'litellm':
        return LITELLM(model_config)
    elif model_config['api_type'] == 'litellm_azure':
        return LITELLM_AZURE(model_config)
    else:
        raise ValueError(f"Unknown model type for {model_name}")