import tkinter as tk
from tkinter import scrolledtext
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import yaml

# ▎Функция создания конфигурации и сохранения в YAML
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


# ▎Функция загрузки конфигурации из YAML
def load_config(filename: str):
    with open(filename, "r", encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)


# ▎Инициализация модели
def initialize_model(config):
    try:
        model_name = config["model"]["name"]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        # Задание устройства (CPU или CUDA)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        print(f"Модель {model_name} успешно загружена на устройство: {device}")
        return tokenizer, model, device
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        exit()


# ▎Генерация текста
def generate_text(input_text: str, model, tokenizer, device, config) -> str:
    try:
        # Параметры из конфигурации
        max_tokens = config["model"]["parameters"]["max_new_tokens"]
        min_tokens = config["model"]["parameters"]["min_new_tokens"]
        num_beams = config["model"]["parameters"]["num_beams"]
        top_p = config["model"]["parameters"]["top_p"]
        temperature = config["model"]["parameters"]["temperature"]
        repetition_penalty = config["model"]["parameters"]["repetition_penalty"]

        # Подготовка ввода
        input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

        # Генерация текста
        output_ids = model.generate(
            input_ids,
            do_sample=True,
            max_length=len(input_ids[0]) + max_tokens,
            min_length=len(input_ids[0]) + min_tokens,
            num_beams=num_beams,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=2,  # Предотвращение повтора фраз
        )

        # Декодирование и возврат текста
        return tokenizer.decode(output_ids[0], skip_special_tokens=True)

    except Exception as e:
        return f"Ошибка при генерации текста: {e}"


# ▎Графический интерфейс (Tkinter)
def create_gui(model, tokenizer, device, config):
    def on_send_message():
        user_message = user_input.get().strip()
        if user_message:
            chat_log.insert(tk.END, f"You → {user_message}\n")
            response = generate_text(user_message, model, tokenizer, device, config)
            chat_log.insert(tk.END, f"Bot → {response}\n\n")
            chat_log.see(tk.END)
            user_input.delete(0, tk.END)

    # Настройка окна
    root = tk.Tk()
    root.title("RuGPT3Small Chatbot")

    # Позволить окну изменять размеры
    root.resizable(True, True)

    # Настройка веса для растягивания компонентов
    root.grid_rowconfigure(0, weight=1)  # Ряд с Frame для чата
    root.grid_columnconfigure(0, weight=1)  # Единственная колонка

    # Чат-лог
    chat_frame = tk.Frame(root)
    chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Добавление веса для масштабирования внутри Frame
    chat_frame.grid_rowconfigure(0, weight=1)
    chat_frame.grid_columnconfigure(0, weight=1)

    chat_log = scrolledtext.ScrolledText(
        chat_frame, 
        wrap=tk.WORD, 
        state="normal", 
        bg="black", 
        fg="white"
    )
    chat_log.grid(row=0, column=0, sticky="nsew")

    # Поле ввода и отправка
    input_frame = tk.Frame(root)
    input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    input_frame.grid_columnconfigure(0, weight=1)

    user_input = tk.Entry(input_frame)
    user_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

    send_button = tk.Button(input_frame, text="Отправка", command=lambda: on_send_message())
    send_button.grid(row=0, column=1)

    # Основной цикл
    root.mainloop()



# ▎Основной блок
if __name__ == "__main__":
    # Создание конфигурационного файла
    config_filename = "config.yaml"
    create_config_file(config_filename)

    # Загрузка конфигурации
    config = load_config(config_filename)

    # Инициализация RuGPT3Small
    tokenizer, model, device = initialize_model(config)

    # Запуск GUI
    create_gui(model, tokenizer, device, config)

