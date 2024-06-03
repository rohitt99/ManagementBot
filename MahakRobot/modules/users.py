from io import BytesIO
from time import sleep
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from telegram import Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
import MahakRobot.modules.no_sql.users_db as user_db
from MahakRobot import pbot as Mukesh, DEV_USERS, LOGGER as logger, OWNER_ID, dispatcher
from MahakRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from MahakRobot.modules.no_sql.users_db import get_all_users
import asyncio, logging, datetime

USERS_GROUP = 4
CHAT_GROUP = 5
DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))

def get_user_id(username):
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = user_db.get_userid_by_name(username)

    if not users:
        return None

    if len(users) == 1:
        return users[0]["_id"]

    for user_obj in users:
        try:
            userdat = dispatcher.bot.get_chat(user_obj["_id"])
            if userdat.username == username:
                return userdat.id
        except BadRequest as excp:
            if excp.message != "❍ ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ":
                logger.exception("❍ ᴇʀʀᴏʀ ᴇxᴛʀᴀᴄᴛɪɴɢ ᴜsᴇʀ ɪᴅ")

    return None

@dev_plus
@Mukesh.on_message(filters.command("bchat") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_chat_handler(bot: Client, m: Message):
    all_chats = user_db.get_all_chats() or []
    await bot.send_message(
        OWNER_ID,
        f"✦ {m.from_user.mention} ɪꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀꜱᴛ......",
    )
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text(f"💌")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_chats = len(user_db.get_all_chats())

    for chat in all_chats:
        sts = await send_chat(chat["chat_id"], broadcast_msg)

        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            pass
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"✦ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ ⏤͟͟͞͞★ \n\n❅ ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ ➠  {total_chats}\n❅ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ➠ {done} / {total_chats}\n❅ sᴜᴄᴄᴇꜱꜱ ➠ {success}\n❅ ғᴀɪʟᴇᴅ ➠ {failed}\n\n✦ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʙʏ ➠ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙ "
            )
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"✦ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ ⏤͟͟͞͞★ {completed_in}.\n\n❅ ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ ➠ {total_chats}\n❅ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ➠ {done} / {total_chats}\n❅ sᴜᴄᴄᴇꜱs ➠ {success}\n❅ ғᴀɪʟᴇᴅ ➠ {failed}\n\n✦ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʙʏ ➠ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙ "
    )

@dev_plus
@Mukesh.on_message(filters.command("buser") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_user_handler(bot: Client, m: Message):
    all_users = get_all_users()
    await bot.send_message(
        OWNER_ID,
        f"✦ {m.from_user.mention} ɪꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀꜱᴛ......",
    )
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text(f"💣")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = len(get_all_users())
    for user in all_users:
        sts = await send_msg(user["_id"], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            pass
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"✦ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ ⏤͟͟͞͞★\n\n❅ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ ➠ {total_users}\n❅ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ➠ {done} / {total_users}\n❅ sᴜᴄᴄᴇss ➠ {success}\n❅ ғᴀɪʟᴇᴅ ➠ {failed}\n\n✦ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʙʏ ➠ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙ "
            )
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"✦ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ⏤͟͟͞͞★\n\n❅ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ ➠ {completed_in}\n❅ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ ➠ {total_users}\n❅ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ➠ {done} / {total_users}\n❅ sᴜᴄᴄᴇss ➠ {success}\n❅ ғᴀɪʟᴇᴅ ➠ {failed}\n\n✦ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʙʏ ➠ ๛ᴍ ᴀ ʜ ᴀ ᴋ ♡゙ "
    )

async def send_chat(chat_id, message):
    try:
        await message.forward(chat_id=int(chat_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_chat(chat_id, message)
    except InputUserDeactivated:
        logger.info(f"❍ {chat_id} ➛ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"❍ {chat_id} ➛ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ")
        return 400
    except
PeerIdInvalid:
        logger.info(f"❍ {chat_id} ➛ ɪᴅ ɪɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.exception(f"❍ {chat_id} ➛ ᴇʀʀᴏʀ: {e}")
        return 500

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"❍ {user_id} ➛ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"❍ {user_id} ➛ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"❍ {user_id} ➛ ɪᴅ ɪɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.exception(f"❍ {user_id} ➛ ᴇʀʀᴏʀ: {e}")
        return 500

@dev_plus
@Mukesh.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(bot: Client, m: Message):
    total_users = len(get_all_users())
    total_chats = len(user_db.get_all_chats())
    await m.reply_text(
        f"📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs:\n\n❅ ᴛᴏᴛᴀʟ ᴜsᴇʀꜱ ➠ {total_users}\n❅ ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ ➠ {total_chats}"
    )

def main():
    dispatcher.add_handler(CommandHandler("bchat", broadcast_chat_handler, Filters.reply))
    dispatcher.add_handler(CommandHandler("buser", broadcast_user_handler, Filters.reply))
    dispatcher.add_handler(CommandHandler("stats", stats_handler))
    dispatcher.start()

if __name__ == "__main__":
    main()


mod_name = "ɢ-ᴄᴀsᴛ"

help = """
 ❍ *ʙʀᴏᴀᴅᴄᴀsᴛ ➛ (ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)*

 ❍ /buser *➛* ʙʀᴏᴀᴅᴄᴀsᴛs ᴛᴏᴏ ᴀʟʟ ᴜsᴇʀs.
 ❍ /bchat *➛* ʙʀᴏᴀᴅᴄᴀsᴛs ᴛᴏᴏ ᴀʟʟ ɢʀᴏᴜᴘs.
 """