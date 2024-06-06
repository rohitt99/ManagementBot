import html
import json
import os
from typing import Optional

from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

from MahakRobot import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    OWNER_ID,
    SUPPORT_CHAT,
    TIGERS,
    WOLVES,
    dispatcher,
)
from MahakRobot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from MahakRobot.modules.helper_funcs.extraction import extract_user
from MahakRobot.modules.log_channel import gloggable

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "MukeshRobot/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "๏ ᴛʜᴀᴛ...ɪs ᴀ ᴄʜᴀᴛ ! ʙᴀᴋᴀ ᴋᴀ ᴏᴍᴀᴇ ?"
    elif user_id == bot.id:
        reply = "๏ ᴛʜɪs ᴅᴏᴇs ɴᴏᴛ ᴡᴏʀᴋ ᴛʜᴀᴛ ᴡᴀʏ."
    else:
        reply = None
    return reply


@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴅʀᴀɢᴏɴ ᴅɪsᴀsᴛᴇʀ")
        return ""

    if user_id in DEMONS:
        rt += "๏ ʀᴇǫᴜᴇsᴛᴇᴅ ʜᴀ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ ᴛᴏ ᴅʀᴀɢᴏɴ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "๏ ʀᴇǫᴜᴇsᴛᴇᴅ ʜᴀ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴀ ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ ᴛᴏ ᴅʀᴀɢᴏɴ."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["sudos"].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\n๏ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ {} ᴛᴏ ᴅʀᴀɢᴏɴ !".format(
            user_member.first_name
        )
    )

    log_message = (
        f"๏ #sᴜᴅᴏ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addsupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "๏ ʀᴇǫᴜᴇsᴛᴇᴅ ʜᴀ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪs ᴅʀᴀɢᴏɴ ᴛᴏ ᴅᴇᴍᴏɴ"
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("๏ ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ.")
        return ""

    if user_id in WOLVES:
        rt += "๏ ʀᴇǫᴜᴇsᴛᴇᴅ ʜᴀ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴛʜɪs ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ ᴛᴏ ᴅᴇᴍᴏɴ"
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["supports"].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n๏ {user_member.first_name} ᴡᴀs ᴀᴅᴅᴇᴅ ᴀs ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ !"
    )

    log_message = (
        f"๏ #sᴜᴘᴘᴏʀᴛ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪs ᴀ ᴅʀᴀɢᴏɴ ᴅɪsᴀsᴛᴇʀ, ᴅᴇᴍᴏᴛɪɴɢ ᴛᴏ ᴡᴏʟғ."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
    rt += "๏ ʀᴇǫᴜᴇsᴛᴇᴅ ʜᴀ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴛʜɪs ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ ᴛᴏ ᴡᴏʟғ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ !")
        return ""

    data["whitelists"].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n๏ {user_member.first_name} ʜᴀs ʙᴇᴇɴ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ᴀs ᴀ ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ !"
    )

    log_message = (
        f"๏ #ᴡʜɪᴛᴇʟɪsᴛ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id not in DRAGONS:
        message.reply_text("๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪsɴ'ᴛ ᴀ ᴅʀᴀɢᴏɴ ᴅɪsᴀsᴛᴇʀ !")
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    data["sudos"].remove(user_id)
    DRAGONS.remove(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        f"๏ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ {user_member.first_name} ғʀᴏᴍ ᴅʀᴀɢᴏɴ ᴅɪsᴀsᴛᴇʀ !"
    )

    log_message = (
        f"๏ #ᴅʀᴀɢᴏɴ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id not in DEMONS:
        message.reply_text("๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪsɴ'ᴛ ᴀ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ !")
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    data["supports"].remove(user_id)
    DEMONS.remove(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        f"๏ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ {user_member.first_name} ғʀᴏᴍ ᴅᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀ !"
    )

    log_message = (
        f"๏ #ᴅᴇᴍᴏɴ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    if user_id not in WOLVES:
        message.reply_text("๏ ᴛʜɪs ᴍᴇᴍʙᴇʀ ɪsɴ'ᴛ ᴀ ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ !")
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    data["whitelists"].remove(user_id)
    WOLVES.remove(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        f"๏ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ {user_member.first_name} ғʀᴏᴍ ᴡᴏʟғ ᴅɪsᴀsᴛᴇʀ !"
    )

    log_message = (
        f"๏ #ᴡᴏʟғ\n"
        f"๏ <b>ᴀᴅᴍɪɴ ➠</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"๏ <b>ᴜsᴇʀ ➠</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"๏ <b>{html.escape(chat.title)}</b>\n" + log_message

    return log_message


__help__ = """
๏ /addsudo <user id> : ᴘʀᴏᴍᴏᴛᴇs ᴀ ᴜsᴇʀ ᴛᴏ ᴅʀᴀɢᴏɴ
๏ /addsupport <user id> : ᴘʀᴏᴍᴏᴛᴇs ᴀ ᴜsᴇʀ ᴛᴏ ᴅᴇᴍᴏɴ
๏ /addwhitelist <user id> : ᴘʀᴏᴍᴏᴛᴇs ᴀ ᴜsᴇʀ ᴛᴏ ᴡᴏʟғ
๏ /removesudo <user id> : ᴅᴇᴍᴏᴛᴇs ᴀ ᴅʀᴀɢᴏɴ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜsᴇʀ
๏ /removesupport <user id> : ᴅᴇᴍᴏᴛᴇs ᴀ ᴅᴇᴍᴏɴ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜsᴇʀ
๏ /removewhitelist <user id> : ᴅᴇᴍᴏᴛᴇs ᴀ ᴡᴏʟғ ᴛᴏ ɴᴏʀᴍᴀʟ ᴜsᴇʀ
"""

__mod_name__ = "ᴀᴅᴠᴀɴᴄᴇᴅ ᴜsᴇʀs"