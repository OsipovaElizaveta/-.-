# -*- coding: cp1251 -*-
from integration import initialize_model
from interface import create_gui
from refactor import create_config_file, load_config

if __name__ == "__main__":
    # Создание конфигурационного файла
    config_filename = "config.yaml"
    create_config_file(config_filename)

    # Загрузка конфигурации
    config = load_config(config_filename)

    # Инициализация модели
    tokenizer, model, device = initialize_model(config)

    # Запуск GUI
    create_gui(model, tokenizer, device, config)