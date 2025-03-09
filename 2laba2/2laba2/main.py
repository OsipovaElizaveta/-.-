from interface import create_gui
from integration import initialize_model, load_config, create_config_file

if __name__ == "__main__":
    # Создание и загрузка конфигурации
    config_filename = "config.yaml"
    create_config_file(config_filename)
    config = load_config(config_filename)

    # Инициализация модели
    tokenizer, model, device = initialize_model(config)

    # Запуск интерфейса
    create_gui(model, tokenizer, device, config)