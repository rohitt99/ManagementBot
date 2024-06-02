import json
import random
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from MahakRobot import dispatcher, OWNER_ID
from MahakRobot.modules.disable import DisableAbleCommandHandler

# Function to fetch a random anime quote
def anime_quote():
    url = "https://animechan.vercel.app/api/random"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        dic = response.json()  # Directly parse JSON response
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching quote: {e}")
        return None, None, None  # Return None if there was an error

    quote = dic.get("quote")
    character = dic.get("character")
    anime = dic.get("anime")
    return quote, character, anime

# Command handler for /quote
def quotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    if quote and character and anime:  # Ensure we have valid data
        msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Change", callback_data="change_quote")]])
        message.reply_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        message.reply_text("Failed to fetch quote. Please try again later.", parse_mode=ParseMode.HTML)

# Callback query handler to change the quote
def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    quote, character, anime = anime_quote()
    if quote and character and anime:  # Ensure we have valid data
        msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Change", callback_data="change_quote")]])
        query.edit_message_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        query.edit_message_text("Failed to fetch quote. Please try again later.", parse_mode=ParseMode.HTML)

# Command handler for /animequotes
def animequotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote_img = random.choice(QUOTES_IMG)
    reply_photo = message.reply_to_message.reply_photo if message.reply_to_message else message.reply_photo
    reply_photo(quote_img)

# List of anime quote images
QUOTES_IMG = [
    "https://i.imgur.com/Iub4RYj.jpg",
    "https://i.imgur.com/uvNMdIl.jpg",
    "https://i.imgur.com/Iub4RYj.jpg",
    "https://i.imgur.com/uvNMdIl.jpg",
    "https://i.imgur.com/YOBOntg.jpg",
    "https://i.imgur.com/fFpO2ZQ.jpg",
    "https://i.imgur.com/f0xZceK.jpg",
    "https://i.imgur.com/RlVcCip.jpg",
    "https://i.imgur.com/CjpqLRF.jpg",
    "https://i.imgur.com/8BHZDk6.jpg",
    "https://i.imgur.com/8bHeMgy.jpg",
    "https://i.imgur.com/5K3lMvr.jpg",
    "https://i.imgur.com/NTzw4RN.jpg",
    "https://i.imgur.com/wJxryAn.jpg",
    "https://i.imgur.com/9L0DWzC.jpg",
    "https://i.imgur.com/sBe8TTs.jpg",
    "https://i.imgur.com/1Au8gdf.jpg",
    "https://i.imgur.com/28hFQeU.jpg",
    "https://i.imgur.com/Qvc03JY.jpg",
    "https://i.imgur.com/gSX6Xlf.jpg",
    "https://i.imgur.com/iP26Hwa.jpg",
    "https://i.imgur.com/uSsJoX8.jpg",
    "https://i.imgur.com/OvX3oHB.jpg",
    "https://i.imgur.com/JMWuksm.jpg",
    "https://i.imgur.com/lhM3fib.jpg",
    "https://i.imgur.com/64IYKkw.jpg",
    "https://i.imgur.com/nMbyA3J.jpg",
    "https://i.imgur.com/7KFQhY3.jpg",
    "https://i.imgur.com/mlKb7zt.jpg",
    "https://i.imgur.com/JCQGJVw.jpg",
    "https://i.imgur.com/hSFYDEz.jpg",
    "https://i.imgur.com/PQRjAgl.jpg",
    "https://i.imgur.com/ot9624U.jpg",
    "https://i.imgur.com/iXmqN9y.jpg",
    "https://i.imgur.com/RhNBeGr.jpg",
    "https://i.imgur.com/tcMVNa8.jpg",
    "https://i.imgur.com/LrVg810.jpg",
    "https://i.imgur.com/TcWfQlz.jpg",
    "https://i.imgur.com/muAUdvJ.jpg",
    "https://i.imgur.com/AtC7ZRV.jpg",
    "https://i.imgur.com/sCObQCQ.jpg",
    "https://i.imgur.com/AJFDI1r.jpg",
    "https://i.imgur.com/TCgmRrH.jpg",
    "https://i.imgur.com/LMdmhJU.jpg",
    "https://i.imgur.com/eyyax0N.jpg",
    "https://i.imgur.com/YtYxV66.jpg",
    "https://i.imgur.com/292w4ye.jpg",
    "https://i.imgur.com/6Fm1vdw.jpg",
    "https://i.imgur.com/2vnBOZd.jpg",
    "https://i.imgur.com/j5hI9Eb.jpg",
    "https://i.imgur.com/cAv7pJB.jpg",
    "https://i.imgur.com/jvI7Vil.jpg",
    "https://i.imgur.com/fANpjsg.jpg",
    "https://i.imgur.com/5o1SJyo.jpg",
    "https://i.imgur.com/dSVxmh8.jpg",
    "https://i.imgur.com/02dXlAD.jpg",
    "https://i.imgur.com/htvIoGY.jpg",
    "https://i.imgur.com/hy6BXOj.jpg",
    "https://i.imgur.com/OuwzNYu.jpg",
    "https://i.imgur.com/L8vwvc2.jpg",
    "https://i.imgur.com/3VMVF9y.jpg",
    "https://i.imgur.com/yzjq2n2.jpg",
    "https://i.imgur.com/0qK7TAN.jpg",
    "https://i.imgur.com/zvcxSOX.jpg",
    "https://i.imgur.com/FO7bApW.jpg",
    "https://i.imgur.com/KK06gwg.jpg",
    "https://i.imgur.com/6lG4tsO.jpg",
    # Add more image URLs as needed
]

# Handlers
ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes)
QUOTES_HANDLER = DisableAbleCommandHandler("quote1", quotes)
CHANGE_QUOTE_HANDLER = CallbackQueryHandler(change_quote, pattern=r"change_quote")

# Add handlers to the dispatcher
dispatcher.add_handler(ANIMEQUOTES_HANDLER)
dispatcher.add_handler(QUOTES_HANDLER)
dispatcher.add_handler(CHANGE_QUOTE_HANDLER)

__mod_name__ = "ǫᴜᴏᴛᴇ"
__help__ = """
❍ /quote ➛ ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴀɴɪᴍᴇ ǫᴜᴏᴛᴇ.
❍ /animequotes ➛ ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴀɴɪᴍᴇ ǫᴜᴏᴛᴇ ɪᴍᴀɢᴇ.
"""

__command_list__ = ["animequotes", "quote"]
__handlers__ = [ANIMEQUOTES_HANDLER, QUOTES_HANDLER, CHANGE_QUOTE_HANDLER]