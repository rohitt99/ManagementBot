from pyrogram import filters
from pyrogram.types import  Message
from pyrogram.types import InputMediaPhoto
from .. import pbot as  Roy, BOT_USERNAME
from MukeshAPI import api
from pyrogram.enums import ChatAction,ParseMode

@Roy.on_message(filters.command("draw"))
async def imagine_(b, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:

        text =message.text.split(None, 1)[1]
    roy=await message.reply_text( "ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ɪᴍᴀɢᴇ...")
    try:
        await b.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        x=api.ai_image(text)
        with open("roy.jpg", 'wb') as f:
            f.write(x)
        caption = f"""
    💘sᴜᴄᴇssғᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ : {text}
    ✨ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ : @{BOT_USERNAME}
    🥀ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
    """
        await roy.delete()
        await message.reply_photo("roy.jpg",caption=caption,quote=True)
    except Exception as e:
        await roy.edit_text(f"error {e}")

