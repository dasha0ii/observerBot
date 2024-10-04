import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import asyncio

# Загрузка данных из .env файла
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Файл для хранения данных пользователей
USER_DATA_FILE = 'users.json'

# Функция для записи пользователя в JSON файл, если его там еще нет
def save_user_to_json(user_id: int):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                users_data = json.load(f)
                if not isinstance(users_data, dict):
                    users_data = {}
            except json.JSONDecodeError:
                users_data = {}
    else:
        users_data = {}

    # Проверяем, есть ли уже этот user_id в базе данных
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {"id": user_id}

        # Записываем обновленные данные в файл
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=4)

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    # Записываем пользователя в базу, если его там еще нет
    save_user_to_json(user_id)

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton('Добавить цель')],
            [KeyboardButton('Уведомления'), KeyboardButton('Мои цели')]
        ],
        resize_keyboard=True
    )

    await message.reply("Привет! Ты записан в базу, если тебя там еще не было.", reply_markup=keyboard)

# Основная функция для запуска
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
