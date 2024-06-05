import os
import time
from gtts import gTTS
import requests
from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode
from MahakRobot import pbot as app


# Define API URL for search
API_URL = "https://sugoi-api.vercel.app/search"

# Command for Bing search
@app.on_message(filters.command(["bing"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def bing_search(app, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ᴛᴏ sᴇᴀʀᴄʜ.")
            return

        keyword = " ".join(message.command[1:])
        params = {"keyword": keyword}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("ɴᴏᴛ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("sᴏʀʀʏ, sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ sᴇᴀʀᴄʜ.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")