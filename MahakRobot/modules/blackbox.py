import requests
from MahakRobot import telethn as tbot
from MahakRobot.events import register


@register(pattern="^/gen (.*)")
async def chat_gpt(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)
    if not query:
        return await event.reply(
            "❍ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ǫᴜᴇʀʏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴏᴅᴇ ᴀғᴛᴇʀ /gen ᴄᴏᴍᴍᴀɴᴅ..\n\n"
            "❍ ғᴏʀ ᴇxᴀᴍᴘʟᴇ ➛ /gen ᴡʀɪᴛᴇ ᴀ ᴄᴏᴅᴇ ғᴏʀ ᴀ sɪᴍᴘʟᴇ ᴘʏᴛʜᴏɴ ᴛᴇʟᴇɢʀᴀᴍ sᴄʀɪᴘᴛ ?"
        )

    processing_message = await event.reply("💭")
    try:
        response = requests.get(f"https://mukesh-api.vercel.app/blackbox?query="
{query}")
        response.raise_for_status()
        result = response.json()
        result.pop("join", None)
        answer = result.get("answer", "❍ ɴᴏ ᴀɴsᴡᴇʀ ʀᴇᴄᴇɪᴠᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʙᴏx ᴀɪ.")
        signature = "\n\n❍ ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛ [ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙](https://t.me/Mahakxbot)"
        await processing_message.edit(answer + signature)
    except requests.RequestException as e:
        await processing_message.edit(f"Error: {str(e)}. Please try again later.")
    except Exception as e:
        await processing_message.edit(f"Unexpected error: {str(e)}. Please try again later.")