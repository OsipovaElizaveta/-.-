import asyncio
from telebot.async_telebot import AsyncTeleBot
from handlers import register_handlers
from utils import load_env_vars

# Загрузка переменных окружения
API_TOKEN = load_env_vars("TELEGRAM_BOT_TOKEN")

# Инициализация бота
bot = AsyncTeleBot(API_TOKEN)

# Регистрация обработчиков
register_handlers(bot)

async def main() -> None:
    """Запуск бота."""
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())