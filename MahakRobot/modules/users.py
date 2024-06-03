from pyrogram import filters
from pyrogram.types import Message
from MahakRobot import pbot as app
from MahakRobot import OWNER_ID
from MahakRobot.modules.helper_funcs.chat_status import dev_plus
import asyncio
import time
import datetime

@dev_plus
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler(bot: app, m: Message):
    broadcast_msg = m.reply_to_message
    broadcast_type = m.text.split("_")[1].strip().lower()  # Extracting broadcast type from the command

    if broadcast_type == "users":
        await broadcast_users(bot, broadcast_msg, m)
    elif broadcast_type == "chats":
        await broadcast_chats(bot, broadcast_msg, m)

async def broadcast_users(bot, broadcast_msg, m):
    all_users = user_db.get_all_users()
    await m.reply_text(f"📣 Broadcasting to all users...")
    start_time = time.time()
    total_users = len(all_users)
    success = 0
    failed = 0

    for user in all_users:
        sts = await send_msg(user["_id"], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await m.reply_text(
        f"✅ Broadcast to all users completed in {completed_in}\nTotal users: {total_users}\nSuccess: {success}\nFailed: {failed}"
    )

async def broadcast_chats(bot, broadcast_msg, m):
    all_chats = user_db.get_all_chats()
    await m.reply_text(f"📣 Broadcasting to all chats...")
    start_time = time.time()
    total_chats = len(all_chats)
    success = 0
    failed = 0

    for chat in all_chats:
        sts = await send_chat(chat["chat_id"], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await m.reply_text(
        f"✅ Broadcast to all chats completed in {completed_in}\nTotal chats: {total_chats}\nSuccess: {success}\nFailed: {failed}"
    )