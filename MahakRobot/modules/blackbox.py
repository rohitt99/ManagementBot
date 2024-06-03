import requests
from MahakRobot import telethn as tbot
from MahakRobot.events import register

BBOX_API_URL = "https://blackai.apinepdev.workers.dev"


@register(pattern="^/gen (.*)")
async def chat_gpt(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)

    if query:
        # Send "Please wait" message
        processing_message = await event.reply("💭")

        try:
            # Make a request to GPT API
            response = requests.get(f"{BBOX_API_URL}/?question={query}")

            if response.status_code == 200:
                # Extract the answer from the API response
                result = response.json()

                # Check if "join" key is present and remove it
                if "join" in result:
                    del result["join"]

                # Add signature to the answer
                answer = result.get("answer", "❍ ɴᴏ ᴀɴsᴡᴇʀ ʀᴇᴄᴇɪᴠᴇᴅ ғʀᴏᴍ ʙʟᴀᴄᴋʙᴏx ᴀɪ.")
                signature = "\n\n❍ ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛ [ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙](https://t.me/Mahakxbot)"
                reply_message = answer + signature

                # Edit the "Please wait" message with the final answer
                await processing_message.edit(reply_message)
            else:
                # If there's an error with the API, inform the user
                await processing_message.edit("Error communicating with ChatGPT API.")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            await processing_message.edit(f"Error: {str(e)}. Please try again later.")
        except Exception as e:
            # Handle unexpected errors
            await processing_message.edit(f"Unexpected error: {str(e)}. Please try again later.")
    else:
        # Provide information about the correct command format
        await event.reply("❍ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ǫᴜᴇʀʏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴏᴅᴇ ᴀғᴛᴇʀ /gen ᴄᴏᴍᴍᴏɴᴅ..\n\n❍ ғᴏʀ ᴇxᴀᴍᴘʟᴇ ➛ /gen ᴡʀɪᴛᴇ ᴀ ᴄᴏᴅᴇ ᴏғ ᴀ sɪᴍᴘʟᴇ ᴘʏᴛʜᴏɴ ᴛᴇʟᴇɢʀᴀᴍ sᴄʀɪᴘᴛ ?")


