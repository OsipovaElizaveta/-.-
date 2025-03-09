# -*- coding: cp1251 -*-
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def setup_client():
    # Загрузка переменных окружения из файла .env
    load_dotenv()
    
    # Получение API-ключа из переменных окружения
    api_key = os.getenv("HF_API_KEY")
    
    # Настройка API клиента Hugging Face
    return InferenceClient(api_key=api_key)
