import logging
from aiogram import Bot, Dispatcher, executor, types
from youtubesearchpython import VideosSearch
from googlesearch import search
import wikipedia

# Sozlamalar
API_TOKEN = '8346712919:AAFLA47hVrc2P7qRRCZOw3zXoUVtCDUh4Ck'
wikipedia.set_lang('uz')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Men universal qidiruv botiman.\nMenga mavzu yozing, men sizga barcha foydali linklarni topib beraman.")

@dp.message_handler()
async def universal_search(message: types.Message):
    query = message.text
    status_msg = await message.answer("Qidirilmoqda... 🔎")

    # 1. Wikipedia ma'lumoti
    try:
        wiki_text = wikipedia.summary(query, sentences=2)
    except:
        wiki_text = "📖 Wikipedia: Ma'lumot topilmadi."

    # 2. YouTube video linki
    try:
        v_search = VideosSearch(query, limit=1)
        v_res = v_search.result()['result']
        video_link = f"🎥 Video: {v_res[0]['link']}" if v_res else "🎥 Video: Topilmadi."
    except:
        video_link = "🎥 Video: Topilmadi."

    # 3. Google linklari (Top 3 ta natija)
    google_links = "🌐 Google natijalari:\n"
    try:
        # Lang="uz" o'zbekcha natijalar uchun
        for j in search(query, num_results=3, lang="uz"):
            google_links += f"- {j}\n"
    except:
        google_links += "Google'dan natija olib bo'lmadi."

    # Hammasini birlashtirish
    response = f"✨ **Natijalar:**\n\n{wiki_text}\n\n{video_link}\n\n{google_links}"
    
    await status_msg.delete()
    await message.answer(response, disable_web_page_preview=False)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
