# -*- coding: cp1251 -*-
import yaml

def create_config_file(filename: str):
    config = {
        "model": {
            "name": "ai-forever/rugpt3small_based_on_gpt2",
            "parameters": {
                "max_new_tokens": 350,
                "min_new_tokens": 250,
                "num_beams": 2,
                "top_p": 0.85,
                "temperature": 1.0,
                "repetition_penalty": 2.0,
            },
        }
    }
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False)
    print("YAML файл успешно создан!")

def load_config(filename: str):
    with open(filename, "r", encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)
