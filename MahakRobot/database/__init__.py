

#MIT License
#Copyright (c) 2023, ©NovaNetworks
from .chatsdb import *
from .usersdb import *

from async_pymongo import AsyncClient

from MahakRobot import MONGO_DB_URI

DBNAME = "MahakRobot"

mongo = AsyncClient(MONGO_DB_URI)
dbname = mongo[DBNAME]

from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from MahakRobot import Aaru 


def is_admins(func: Callable) -> Callable:
    async def non_admin(c: Ravan, m: Message):
        if m.from_user.id == OWNER:
            return await func(c, m)

        admin = await c.get_chat_member(m.chat.id, m.from_user.id)
        if admin.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await func(c, m)

    return non_admin
