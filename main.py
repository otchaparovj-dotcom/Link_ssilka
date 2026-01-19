import logging
import openai
from aiogram import Bot, Dispatcher, executor, types

# Sozlamalar
API_TOKEN = '8346712919:AAFLA47hVrc2P7qRRCZOw3zXoUVtCDUh4Ck'
openai.api_key = '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'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Men ChatGPT asosida ishlaydigan aqlli botman. Savolingizni yozing!")

@dp.message_handler()
async def chat_gpt_answer(message: types.Message):
    status = await message.answer("O'ylayapman... 🧠")
    
    try:
        # ChatGPT so'rovi
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message.content
        
        await status.delete()
        await message.answer(answer)
    except Exception as e:
        logging.error(e)
        await status.edit_text("Hozircha javob bera olmayman (API cheklovi yoki xatolik).")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
