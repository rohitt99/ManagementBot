#MIT License
#Copyright (c) 2023, ©NovaNetworks
from .chatsdb import *
from .usersdb import *

from async_pymongo import AsyncClient

from MahakRobot import MONGO_DB_URI

DBNAME = "MahakRobot"

mongo = AsyncClient(MONGO_DB_URI)
dbname = mongo[DBNAME]
