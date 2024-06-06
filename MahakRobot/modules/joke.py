import requests
from MahakRobot import pbot as app
from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/mahakxbot?startgroup=true"),
    ],
]

JOKE_API_ENDPOINT = 'https://hindi-jokes-api.onrender.com/jokes?api_key=1a6d440e3f5971eecebceee818c2'

@app.on_message(filters.command("joke"))
async def joke(_, message):
    response = requests.get(JOKE_API_ENDPOINT)
    r = response.json()
    joke_text = r['jokeContent']
    await message.reply_text(joke_text)


#    await message.reply_text(joke_text, caption=f"❖ ᴊᴏᴋᴇs ʙʏ ➥ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙", reply_markup=InlineKeyboardMarkup(EVAA),)

__help__ = """

❍ /joke  *➛* ɢᴇɴᴇʀᴀᴛᴇ ᴀ ʀᴀɴᴅᴏᴍ ᴊᴏᴋᴇ.

"""
__mode_name__ = "ᴊᴏᴋᴇ"

