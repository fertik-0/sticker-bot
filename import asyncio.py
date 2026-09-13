import asyncio
import time
from collections import defaultdict
from aiogram import Bot, Dispatcher, F, types

# Укажите ваш токен от BotFather
TOKEN = "7464632988:AAHjuEvu_tU1SZDsSg5kbgthSnbKbM2VgvQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище в оперативной памяти: user_id -> [timestamp1, timestamp2, ...]
user_stickers = defaultdict(list)

MAX_STICKERS = 2        # Максимум стикеров
TIME_WINDOW = 3600      # Окно ограничения в секундах (1 час)

@dp.message(F.sticker)
async def handle_sticker(message: types.Message):
    user_id = message.from_user.id
    now = time.time()
    
    # Очищаем метки времени старше 1 часа
    user_stickers[user_id] = [t for t in user_stickers[user_id] if now - t < TIME_WINDOW]
    
    if len(user_stickers[user_id]) >= MAX_STICKERS:
        try:
            # Удаляем превышающий лимит стикер
            await message.delete()
            
            # Опционально: отправляем временное предупреждение
            warning = await message.answer(
                f"⚠️ {message.from_user.mention_html()}, лимит стикеров — {MAX_STICKERS} в час!",
                parse_mode="HTML"
            )
            await asyncio.sleep(5)
            await warning.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    else:
        # Фиксируем время успешной отправки
        user_stickers[user_id].append(now)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())