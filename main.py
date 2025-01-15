import asyncio

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user_handlers
import logging
import os

# Настройка логирования
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/bot.log"),
        logging.StreamHandler()  # Логи также выводятся в консоль
    ]
)

# Функция конфигурирования и запуска бота
async def main():
    logging.info("Bot initialization...")
    # Инициализируем бот и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        logging.info("Bot launching...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot is turned off")
