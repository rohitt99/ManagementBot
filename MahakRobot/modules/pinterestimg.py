import requests
from requests import get
from MahakRobot import pbot as app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto

@app.on_message(filters.command(["pntimg"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def pinterest(_, message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("**ɢɪᴠᴇ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍**")

    try:
        images = get(f"https://aiimage.hellonepdevs.workers.dev/?prompt={query}&state=url").json()
    except Exception as e:
        return await message.reply(f"**Failed to fetch images: {e}**")

    media_group = []
    count = 0

    msg = await message.reply("sᴄʀᴀᴘɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴘɪɴᴛᴇʀᴇsᴛ...")

    for url in images.get("images", [])[:6]:
        media_group.append(InputMediaPhoto(media=url))
        count += 1
        await msg.edit(f"=> ᴏᴡᴏ sᴄʀᴀᴘᴇᴅ ɪᴍᴀɢᴇs {count}")

    try:
        await app.send_media_group(
            chat_id=chat_id, 
            media=media_group,
            reply_to_message_id=message.id
        )
        await msg.delete()
    except Exception as e:
        await msg.delete()
        await message.reply(f"ᴇʀʀᴏʀ : {e}")
