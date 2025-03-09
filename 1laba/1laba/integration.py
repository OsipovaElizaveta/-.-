# -*- coding: cp1251 -*-
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

def setup_client():
    # �������� ���������� ��������� �� ����� .env
    load_dotenv()
    
    # ��������� API-����� �� ���������� ���������
    api_key = os.getenv("HF_API_KEY")
    
    # ��������� API ������� Hugging Face
    return InferenceClient(api_key=api_key)
