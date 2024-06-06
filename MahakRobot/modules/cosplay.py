import requests
from pyrogram import filters
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.enums import ChatAction
from MahakRobot import pbot as app
from MahakRobot import BOT_USERNAME

MAHAK = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/mahakxbot?startgroup=true"),
    ],
]

@app.on_message(filters.command("cosplay"))
async def cosplay(_,msg):
    img = requests.get("https://waifu-api.vercel.app").json()
    await msg.reply_photo(img, caption=f"❅ ᴄᴏsᴘʟᴀʏ ʙʏ ➠ ‌ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙", reply_markup=InlineKeyboardMarkup(MAHAK),)

__help__ = """

❍ /cosplay *➛* ɢᴇɴᴇʀᴀᴛᴇ ᴀ ʀᴀɴᴅᴏᴍ ᴄᴏsᴘʟᴀʏ ɪᴍᴀɢᴇ.

"""
__mode_name__ = "ᴄᴏsᴘʟᴀʏ"