import asyncio
import os
import time
from collections import defaultdict
from aiogram import Bot, Dispatcher, F, types

# Бот безопасно забирает токен из настроек сервера
TOKEN = os.getenv("7464632988:AAHjuEvu_tU1SZDsSg5kbgthSnbKbM2VgvQ")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_stickers = defaultdict(list)

MAX_STICKERS = 2
TIME_WINDOW = 3600

@dp.message(F.sticker)
async def handle_sticker(message: types.Message):
    user_id = message.from_user.id
    now = time.time()
    
    user_stickers[user_id] = [t for t in user_stickers[user_id] if now - t < TIME_WINDOW]
    
    if len(user_stickers[user_id]) >= MAX_STICKERS:
        try:
            await message.delete()
            
            warning = await message.answer(
                f"⚠️ {message.from_user.mention_html()}, лимит стикеров — {MAX_STICKERS} в час!",
                parse_mode="HTML"
            )
            await asyncio.sleep(5)
            await warning.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    else:
        user_stickers[user_id].append(now)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
