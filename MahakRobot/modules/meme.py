import logging
import random
import requests
from telethon import events
from MahakRobot import telethn as meow

logging.basicConfig(level=logging.DEBUG)

MemesReddit = [
    "Animemes",
    "lostpause",
    "LoliMemes",
    "cleananimemes",
    "animememes",
    "goodanimemes",
    "AnimeFunny",
    "dankmemes",
    "teenagers",
    "shitposting",
    "Hornyjail",
    "wholesomememes",
    "cursedcomments",
]

async def fetch_meme(event, subreddit=None):
    try:
        if not subreddit:
            subreddit = random.choice(MemesReddit)
        meme_link = f"https://meme-api.com/gimme/{subreddit}"
        response = requests.get(meme_link)
        
        # Log the entire JSON response for debugging
        logging.debug(f"API Response: {response.text}")
        
        q = response.json()

        # Check for expected keys in the response
        if 'title' in q and 'url' in q:
            await event.reply(q["title"], file=q["url"])
        else:
            logging.error(f"Missing expected keys in response: {q}")
            await event.reply("Sorry, couldn't fetch a meme at the moment.")
    except Exception as e:
        logging.error(f"Error fetching meme: {e}")
        await event.reply("Sorry, couldn't fetch a meme at the moment.")

@meow.on(events.NewMessage(pattern="^/memes"))
async def memes_handler(event):
    await fetch_meme(event)

@meow.on(events.NewMessage(pattern="^/dank"))
async def dank_handler(event):
    await fetch_meme(event, "dankmemes")

@meow.on(events.NewMessage(pattern="^/lolimeme"))
async def lolimeme_handler(event):
    await fetch_meme(event, "LoliMemes")

@meow.on(events.NewMessage(pattern="^/hjail"))
async def hjail_handler(event):
    await fetch_meme(event, "Hornyjail")

@meow.on(events.NewMessage(pattern="^/wmeme"))
async def wmeme_handler(event):
    await fetch_meme(event, "wholesomememes")

@meow.on(events.NewMessage(pattern="^/pewds"))
async def pewds_handler(event):
    await fetch_meme(event, "PewdiepieSubmissions")

@meow.on(events.NewMessage(pattern="^/hmeme"))
async def hmeme_handler(event):
    await fetch_meme(event, "hornyresistance")

@meow.on(events.NewMessage(pattern="^/teen"))
async def teen_handler(event):
    await fetch_meme(event, "teenagers")

@meow.on(events.NewMessage(pattern="^/fbi"))
async def fbi_handler(event):
    await fetch_meme(event, "FBI_Memes")

@meow.on(events.NewMessage(pattern="^/shitposting"))
async def shitposting_handler(event):
    await fetch_meme(event, "shitposting")

@meow.on(events.NewMessage(pattern="^/cursed"))
async def cursed_handler(event):
    await fetch_meme(event, "cursedcomments")

__help__ = """
❍ /joke *➛* ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴊᴏᴋᴇs.