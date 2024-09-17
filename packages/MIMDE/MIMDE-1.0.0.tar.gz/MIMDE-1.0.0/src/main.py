from response_mapping import response_Brute_force_pipeline
from theme_extraction import themes_Brute_force_pipeline
import yaml
import argparse
import LLMs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="")
    args = parser.parse_args()
    if args.config=="":
        raise ValueError('Please provide a path to your config file using python Brute_force.py --config your_config_file_path')
    ### model configuration
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)
    demo = dict(config['DEMO'])
    models = config['MODELS']
    consultation_name = config['CONSULTATIONS'][0]
    for model_name in models:
        #for consultation_name in consultation_name s:
        print(f"Analyzing {consultation_name} with model {model_name}")
        #response_Brute_force_pipeline(demo, consultation_name, model_name)
        themes_Brute_force_pipeline(demo, consultation_name, model_name)
        print("Brute force pipeline completed successfully for consultation: ", consultation_name)
