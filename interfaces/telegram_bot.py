import os, asyncio
import logging
from aiogram import Bot, Dispatcher, types
from ask import handle_message
from dotenv import load_dotenv; load_dotenv()

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

bot = Bot(os.getenv("BOT_TOKEN"))
dp  = Dispatcher()

@dp.message()
async def on_msg(msg: types.Message):
    print(msg.text)
    reply = await handle_message(msg.text)
    await msg.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
