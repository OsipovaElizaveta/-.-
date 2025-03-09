import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
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
    print("YAML file created successfully!")

def load_config(filename: str):
    with open(filename, "r", encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)

def initialize_model(config):
    try:
        model_name = config["model"]["name"]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        print(f"model {model_name} successfully loaded to device: {device}")
        return tokenizer, model, device
    except Exception as e:
        print(f"Model loading error: {e}")
        exit()

def generate_text(input_text: str, model, tokenizer, device, config) -> str:
    try:
        max_tokens = config["model"]["parameters"]["max_new_tokens"]
        min_tokens = config["model"]["parameters"]["min_new_tokens"]
        num_beams = config["model"]["parameters"]["num_beams"]
        top_p = config["model"]["parameters"]["top_p"]
        temperature = config["model"]["parameters"]["temperature"]
        repetition_penalty = config["model"]["parameters"]["repetition_penalty"]

        input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

        output_ids = model.generate(
            input_ids,
            do_sample=True,
            max_length=len(input_ids[0]) + max_tokens,
            min_length=len(input_ids[0]) + min_tokens,
            num_beams=num_beams,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=2,
        )

        return tokenizer.decode(output_ids[0], skip_special_tokens=True)

    except Exception as e:
        return f"Error when generating text: {e}"