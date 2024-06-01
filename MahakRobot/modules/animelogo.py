from pyrogram.types import Message
import random
from pyrogram import Client, filters, idle
import pyrogram, asyncio, random, time
from pyrogram.errors import FloodWait
import requests
from MahakRobot import pbot as app 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#######

button = [
       [
            InlineKeyboardButton(
                text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/MahakXbot?startgroup=true",
            )
        ]
]

#####



@app.on_message(filters.command("animelogo"))
async def logo(app, msg: Message):
    if len(msg.command) == 1:
       return await msg.reply_text("✦ ᴜsᴀɢᴇ ➥ /animelogo Mahak")
    logo_name = msg.text.split(" ", 1)[1]
    API = f"https://api.sdbots.tech/anime-logo?name={logo_name}"
    req = requests.get(API).url
    await msg.reply_photo(
        photo=f"{req}",
        caption=f"❖ ᴀɴɪᴍᴇ ʟᴏɢᴏ ʙʏ ➥ [๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙](https://t.me/Ravan_Lankaa)",
        reply_markup=InlineKeyboardMarkup(button),
    )


__mod_name__ = "ᴀɴɪᴍᴇ-ʟᴏɢᴏ"

__help__ = """

 ❍ /animelogo ➛ ᴄʀᴇᴀᴛᴇ ᴏᴡɴ ᴛᴇxᴛ ᴀɴɪᴍᴇ ʟᴏɢᴏ ᴡɪᴛʜ ɴʏᴋᴀᴀ.
 """


