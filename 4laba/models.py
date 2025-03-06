from huggingface_hub import InferenceClient
from utils import load_env_vars

# Загрузка переменных окружения
HUGGING_FACE_API_TOKEN = load_env_vars("HUGGING_FACE_API_TOKEN")

# Инициализация Hugging Face Inference Client
client = InferenceClient(api_key=HUGGING_FACE_API_TOKEN)

# Переменная для хранения выбранной модели
current_model: str = "meta-llama/Llama-3.2-3B-Instruct"  # Llama-3.2-3B-Instruct

def set_model(model_name: str) -> None:
    """
    Устанавливает текущую модель для генерации ответов.

    Аргументы:
        model_name (str): Название модели.
    """
    global current_model
    current_model = model_name

def generate_response(prompt: str) -> str:
    """
    Генерирует ответ на запрос пользователя с использованием текущей модели.

    Аргументы:
        prompt (str): Запрос пользователя.

    Возвращает:
        str: Ответ модели.
    """
    response = client.text_generation(
        prompt=prompt,
        model=current_model,
        max_new_tokens=700,
        temperature=0.7,
        top_k=50,
        do_sample=True,
    )
    return response