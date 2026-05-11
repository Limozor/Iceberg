import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from API import Telegram_API

last_photo_filename = None

bot = Bot(token=Telegram_API)
dp = Dispatcher(storage=MemoryStorage())

emoji = {"Автомат": "🎰",
         "Кубик": "🎲",
         "Мишень": "🎯",
         "Баскетбол": "🏀",
         "Футбол": "⚽️",
         "Боулинг": "🎳"
          }

class FileWait(StatesGroup):
    file = State()

class Algorithm(StatesGroup):

 @dp.message(Command("start"))
 async def start_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"""
    (⊙_⊙;)
Добро пожаловать {message.from_user.full_name} в Айсберг
выберите команду для использования нужного сервиса""")
    await message.answer("""Доступные команды:
    /start - перезапуск
    /checkfile - Проверка файла 
    /games - Игры
    /info - О нас 
    /ts - техподдержка
    /id - информация о вас
    """)

 @dp.message(Command("checkfile"))
 async def file_message(message: Message, state: FSMContext):
     await message.answer("Отправьте файл для проверки")
     await state.set_state(FileWait.file)

 @dp.message(FileWait.file, F.document)
 async def process_file(message: Message, bot: Bot, state: FSMContext):
     global last_photo_filename

     doc = message.document
     file_name = doc.file_name if doc.file_name else f"{doc.file_unique_id}.bin"

     script_dir = os.path.dirname(os.path.abspath(__file__))
     download_dir = os.path.join(script_dir, "downloads")
     os.makedirs(download_dir, exist_ok=True)

     path = os.path.join(download_dir, file_name)
     await bot.download(doc, destination=path)

     last_photo_filename = file_name
     await message.answer("Начат процесс проверки")
     await state.clear()


 @dp.message(Command("games"))
 async def games_menu(message: types.Message, state: FSMContext):
     await state.clear()
     builder = InlineKeyboardBuilder()
     for data, text in emoji.items():
         builder.button(text=text, callback_data=data)
     builder.adjust(3)
     await message.answer("Выберите игру:", reply_markup=builder.as_markup())

 @dp.callback_query(F.data.in_(emoji.keys()))
 async def games_answer(callback: types.CallbackQuery):
     await callback.answer()
     response = emoji[callback.data]
     await callback.message.answer_dice(emoji=response)


 @dp.message(Command("info"))
 async def info_message(message: Message, state: FSMContext):
    await state.clear()


 @dp.message(Command("ts"))
 async def ts_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("""Для получения технической поддержки обратитесь к:
    @Limozor""")


 @dp.message(Command("id"))  # только текст добавить
 async def id_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(message.from_user.full_name)
    await message.answer(str(message.from_user.username))
    await message.answer(str(message.from_user.id))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Бот начал работу")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Бот завершил работу")