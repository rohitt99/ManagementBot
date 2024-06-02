import requests
from MahakRobot import pbot as app
from pyrogram import filters
from pyrogram.types import InputMediaPhoto

# Extract search query from message
def extract_query(message):
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None

# Generate image using AI image generation API
def generate_image(prompt):
    try:
        response = requests.get(f"https://ai.hellonepdevs.workers.dev/?prompt={prompt}&image=1")
        response.raise_for_status()
        data = response.json()
        if "image_url" in data:
            return data["image_url"]
        else:
            return "No image generated."
    except (requests.RequestException, ValueError) as e:
        return str(e)

@app.on_message(filters.command(["aiimg"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def ai_image(_, message):
    chat_id = message.chat.id

    # Extract prompt
    prompt = extract_query(message)
    if not prompt:
        return await message.reply("**Please provide a prompt for the image generation.**")

    # Generate image
    result = generate_image(prompt)
    if isinstance(result, str):
        return await message.reply(f"**{result}**")
    image_url = result

    # Inform user and send generated image
    msg = await message.reply("Generating image...")

    try:
        await app.send_photo(chat_id=chat_id, photo=image_url, reply_to_message_id=message.id)
        await msg.delete()
    except Exception as e:
        await msg.edit(f"Error: {e}")

# Start the app (if not already running in your main file)
if __name__ == "__main__":
    app.run()