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

# Fetch image URLs from the API
def fetch_images(query):
    try:
        response = requests.get(f"https://aiimage.hellonepdevs.workers.dev/?prompt={query}&state=url")
        response.raise_for_status()
        return response.json().get("images", [])
    except (requests.RequestException, ValueError) as e:
        return str(e)

# Prepare media group for sending
def prepare_media_group(image_urls):
    media_group = [InputMediaPhoto(media=url) for url in image_urls[:6]]
    return media_group

@app.on_message(filters.command(["pntimg"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def pinterest(_, message):
    chat_id = message.chat.id

    # Extract query
    query = extract_query(message)
    if not query:
        return await message.reply("**Please provide an image name for the search 🔍**")

    # Fetch images
    result = fetch_images(query)
    if isinstance(result, str):
        return await message.reply(f"**Failed to fetch images: {result}**")
    image_urls = result

    # Prepare media group
    media_group = prepare_media_group(image_urls)
    if not media_group:
        return await message.reply("**No images found.**")

    # Inform user and send media group
    msg = await message.reply("Scraping images from Pinterest...")
    for count, media in enumerate(media_group, 1):
        await msg.edit(f"=> Scraped {count} images")
    
    try:
        await app.send_media_group(chat_id=chat_id, media=media_group, reply_to_message_id=message.id)
        await msg.delete()
    except Exception as e:
        await msg.delete()
        await message.reply(f"Error: {e}")