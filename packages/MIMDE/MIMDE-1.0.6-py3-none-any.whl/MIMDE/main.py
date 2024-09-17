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
 
    themes_Brute_force_pipeline(args.config)
    print("Brute force pipeline completed successfully for consultation: ")
