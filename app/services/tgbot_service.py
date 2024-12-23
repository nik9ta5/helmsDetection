import os 
import json
import asyncio
from aiogram import Bot
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InputFile
from aiogram.types.input_file import FSInputFile

def write_to_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 для читабельности


# Функция для чтения данных из JSON файла
def read_from_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


TOKEN = os.getenv('toketBotTG')
if not TOKEN:
    raise ValueError("Токен Telegram бота не найден!")



CHAT_IDS_ALL_USERS_BOT = []
BOT = Bot(token=TOKEN)
DP = Dispatcher()


# async def send_message_to_user(chat_id: int, message: str):
#     timeout = asyncio.Timeout(10)
#     async with timeout:
#         await BOT.send_message(chat_id=chat_id, text=message)


async def send_message_to_user(chat_id: int, message: str):
    try:
        await BOT.send_message(chat_id=chat_id, text=message)
        print(f"Message sent to {chat_id}: {message}")
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {e}")


async def send_photo_to_user(chat_id: int, photo_path: str, caption: str = ""):
    try:
        photo = FSInputFile(photo_path, filename=os.path.basename(photo_path))
        # photo = InputFile(path_or_bytesio=photo_path)  
        await BOT.send_photo(chat_id=chat_id, photo=photo, caption=caption)
    except Exception as e:
        print(f"Failed to send photo to {chat_id}: {e}")


@DP.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.id not in CHAT_IDS_ALL_USERS_BOT:
        CHAT_IDS_ALL_USERS_BOT.append(message.chat.id)
    print(CHAT_IDS_ALL_USERS_BOT)
    await message.answer("Вы подписались на получение уведомлений при обнаружении человека без каски на предприятии.")


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(f"Вы написали: {message.text}")


async def bot_service_run():
    print("RUNNING BOT")
    await DP.start_polling(BOT)
    print("BOT ENDING")