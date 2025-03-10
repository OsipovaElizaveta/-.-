import os
from typing import Optional, List
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from natasha import MorphVocab

import unicodedata
import logging

logging.basicConfig(level=logging.DEBUG)

# Инициализация морфологического словаря
morph_vocab = MorphVocab()

def load_env_vars(key: str) -> str:
    """
    Загружает переменную окружения по ключу.

    Аргументы:
        key (str): Ключ переменной окружения.

    Возвращает:
        str: Значение переменной окружения.

    Исключения:
        ValueError: Если переменная окружения не найдена.
    """
    load_dotenv(".env")
    
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Переменная окружения {key} не найдена.")
    return value

def create_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с основными командами для пользователя.

    Возвращает:
        ReplyKeyboardMarkup: Объект клавиатуры с кнопками.
    """
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(
        KeyboardButton("Расписание"),
        KeyboardButton("Напоминания"),
        KeyboardButton("Поиск материалов"),
        KeyboardButton("Задать вопрос"),
        KeyboardButton("Выбрать модель"),
    )
    return markup

def normalize_text(text: str) -> str:
    """
    Нормализовать текст, чтобы обеспечить согласованное сравнение.
    """
    return unicodedata.normalize('NFKC', text)

def is_educational_message(message_text: str) -> bool:
    """
    Проверяет, связано ли сообщение с учебой, используя список ключевых слов и Natasha для учета склонений.
    """
    # Чтение ключевых слов из файла
    try:
        with open("educational_keywords.txt", "r", encoding="utf-8") as file:
            educational_keywords = [
                normalize_text(line.strip().lower()) for line in file.readlines() if line.strip()
            ]
    except FileNotFoundError:
        logging.error("Файл educational_keywords.txt не найден.")
        return False
    
    if not educational_keywords:
        logging.error("Файл с ключевыми словами пуст.")
        return False

    # Приведение текста сообщения к нижнему регистру и нормализация
    message_text = normalize_text(message_text.lower())
    
    # Разбиваем сообщение на слова
    user_words = message_text.split()
    
    for word in user_words:
        # Приводим слово к начальной форме (лемматизация)
        parsed_word = morph_vocab(word)  # Вернуть список объектов MorphForm
        
        if parsed_word:  # Убедиться что список не пуст
            # Вытаскиваем нормальные формы слова как string
            normal_forms = [form.normal_form for form in parsed_word if hasattr(form, 'normal_form')]
            
            # Проверить все нормальные формы слова
            for normal_form in normal_forms:
                normal_form = normalize_text(normal_form)
                
                # Логирование normal_form для дебага
                logging.debug(f"Word: {word}, Normal Form: {normal_form}")
                
                # Проверяем, есть ли начальная форма в списке ключевых слов
                if normal_form in educational_keywords:
                    return True
    
    return False