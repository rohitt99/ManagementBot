from pyrogram import Client, filters
import requests
from MahakRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

EVAA = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/mahakxbot?startgroup=true"),
    ],
]

# URL for the Bored API
bored_api_url = "https://apis.scrimba.com/bored/api/activity"


# Function to handle /bored command
@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(client, message):
    # Fetch a random activity from the Bored API
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            # Send the activity to the user who triggered the command
            await message.reply(f"❖ ғᴇᴇʟɪɴɢ ʙᴏʀᴇᴅ ? ʜᴏᴡ ᴀʙᴏᴜᴛ ⏤‌★\n\n● `{activity}`\n\n❖ ғᴇᴇʟɪɴɢ ʙʏ ➥ [๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙](htps://t.me/mahakxbot)", reply_markup=InlineKeyboardMarkup(EVAA),)
        else:
            await message.reply("✦ ɴᴏ ᴀᴄᴛɪᴠɪᴛʏ ғᴏᴜɴᴅ.")
    else:
        await message.reply("✦ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴀᴄᴛɪᴠɪᴛʏ.")

__mod_name__ = "ʙᴏʀᴇᴅ"
__help__ = """


❍ /bored ➛ ᴀʀᴇ ʏᴏᴜ ғᴇᴇʟɪɴɢ ʙᴏʀᴇᴅ ʀᴜɴ ᴛʜɪs ᴄᴏᴍᴍᴏɴᴅs.
 """