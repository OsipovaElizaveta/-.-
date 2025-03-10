from typing import Dict, List
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from models import set_model, generate_response, current_model
from utils import create_menu_keyboard, is_educational_message

# Пример расписания
schedule: Dict[str, List[str]] = {
    "Понедельник": ["Математика - 10:00", "Физика - 12:00"],
    "Вторник": ["Программирование - 9:00", "Английский - 14:00"],
}

# Пример дедлайнов
deadlines: Dict[str, str] = {
    "Лабораторная работа по Python": "2023-12-15",
    "Экзамен по математике": "2023-12-20",
}

# Словарь для сопоставления названий кнопок с именами моделей
model_mapping: Dict[str, str] = {
    "LLaMA": "meta-llama/Llama-3.2-3B-Instruct",
    "ruGPT-3": "ai-forever/rugpt3small_based_on_gpt2",  # Обновлено на новую модель
}

def register_handlers(bot: AsyncTeleBot) -> None:
    """
    Регистрирует обработчики команд и сообщений.
    Аргументы:
        bot (AsyncTeleBot): Экземпляр бота.
    """

    @bot.message_handler(commands=['start'])
    async def send_welcome(message: types.Message) -> None:
        # Обработчик команды /start
        await bot.send_message(
            message.chat.id,
            "Привет! Я твой помощник для учебы. Чем могу помочь?",
            reply_markup=create_menu_keyboard(),
        )

    @bot.message_handler(func=lambda message: message.text == "Расписание")
    async def show_schedule(message: types.Message) -> None:
        # Обработчик нажатия на "Расписание"
        today = "Понедельник"  # Замените на реальное определение дня
        if today in schedule:
            await bot.send_message(
                message.chat.id,
                f"Расписание на сегодня:\n" + "\n".join(schedule[today]),
            )
        else:
            await bot.send_message(message.chat.id, "Сегодня занятий нет.")

    @bot.message_handler(func=lambda message: message.text == "Напоминания")
    async def show_deadlines(message: types.Message) -> None:
        # Обработчик нажатия на "Напоминания"
        reminders = [f"{task}: {date}" for task, date in deadlines.items()]
        await bot.send_message(
            message.chat.id,
            "Ваши дедлайны:\n" + "\n".join(reminders),
        )

    @bot.message_handler(func=lambda message: message.text == "Выбрать модель")
    async def choose_model(message: types.Message) -> None:
        # Обработчик нажатия на "Выбрать модель"
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(*[types.KeyboardButton(model_name) for model_name in model_mapping.keys()])
        await bot.send_message(
            message.chat.id,
            "Выберите модель для ответов на вопросы:",
            reply_markup=markup,
        )

    @bot.message_handler(func=lambda message: message.text in model_mapping.keys())
    async def handle_model_selection(message: types.Message) -> None:
        # Обработчик выбора модели
        selected_model_name = model_mapping.get(message.text, None)
        if selected_model_name:
            set_model(selected_model_name)
            await bot.send_message(
                message.chat.id,
                f"Теперь используется модель {message.text}.",
                reply_markup=create_menu_keyboard(),
            )
        else:
            await bot.send_message(
                message.chat.id,
                "Неизвестная модель. Пожалуйста, выберите модель из списка.",
                reply_markup=create_menu_keyboard(),
            )

    @bot.message_handler(func=lambda message: True)
    async def handle_message(message: types.Message) -> None:
        # Обработчик текстовых сообщений
        user_input = message.text
        if is_educational_message(user_input):
            try:
                await bot.send_chat_action(message.chat.id, "typing")
                response = generate_response(user_input)
                await bot.send_message(message.chat.id, f"Ответ:\n{response}")
            except Exception as e:
                await bot.send_message(message.chat.id, f"Ошибка при запросе к модели: {str(e)}")
        else:
            await bot.send_message(message.chat.id, "Пожалуйста, задавайте вопросы, связанные с учебой.")