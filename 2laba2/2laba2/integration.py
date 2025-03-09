# -*- coding: cp1251 -*-
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def initialize_model(config):
    try:
        model_name = config["model"]["name"]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        print(f"������ {model_name} ������� ��������� �� ����������: {device}")
        return tokenizer, model, device
    except Exception as e:
        print(f"������ �������� ������: {e}")
        exit()
