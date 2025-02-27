import logging
import os
import sys
import time
import spamwatch
import httpx
import aiohttp
import telegram.ext as tg

from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.sessions import StringSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat


StartTime = time.time()

# enable logging

#print(flag)
log = logging.getLogger('[Enterprise]')
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)
log.info("[KIGYO] Kigyo is starting. | An Eagle Union Project. | Licensed under GPLv3.")
log.info("[KIGYO] Not affiliated to Azur Lane or Yostar in any way whatsoever.")
log.info("[KIGYO] Project maintained by: github.com/Dank-del (t.me/dank_as_fuck)")

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", 2079472115))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
        
    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", False)) # Info Pic (use True[Value] If You Want To Show In /info.)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None) # G-Ban Logs (Channel) (-100)
    ERROR_LOGS = os.environ.get("ERROR_LOGS", None) # Error Logs (Channel Ya Group Choice Is Yours) (-100)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # If You Deploy On Heraku. [URL PERTEN:- https://{App Name}.herokuapp.com/ || EXP:- https://yuki-REM-robot.herokuapp.com/]
    PORT = int(os.environ.get("PORT", 8443)) 
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None) # Bot Owner's API_ID (From:- https://my.telegram.org/auth)
    API_HASH = os.environ.get("API_HASH", None) # Bot Owner's API_HASH (From:- https://my.telegram.org/auth)
    DB_URL = os.environ.get("DB_URL") # Any SQL Database Link (RECOMMENDED:- PostgreSQL & https://www.elephantsql.com)
    DONATION_LINK = os.environ.get("DONATION_LINK") # Donation Link (ANY)
    ALONE_ID = os.environ.get("ALONE_ID", 5297261589)
    LOAD = os.environ.get("LOAD", "").split() # Don't Change
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split() # Don't Change
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False)) # Don't Change
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True)) # Use `True` Value
    WORKERS = int(os.environ.get("WORKERS", 8)) # Don't Change
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg") # Don't Change
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False) # Don't Change
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./") # Don't Change
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None) # From:- https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None) # From:- https://timezonedb.com/api
    WALL_API = os.environ.get("WALL_API", None) # From:- https://wall.alphacoders.com/api.php
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None) # From:- https://www.remove.bg/
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "") # From:- https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", None) # From:- http://genius.com/api-clients
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", None) # MongoDB URL (From:- https://www.mongodb.com/)
    REDIS_URL = os.environ.get("REDIS_URL", None) # REDIS URL (From:- Heraku & Redis)
    BOT_ID = int(os.environ.get("BOT_ID", None)) # Telegram Bot ID (EXP:- 1241223850)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None) # Support Chat Group Link (Use @Black_Knights_Union_Support || Dont Use https://t.me/Black_Knights_Union_Support)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None) # Use @SpamWatchSupport
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None) # From https://t.me/SpamWatchBot 
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # Bot Username
    STRING_SESSION = os.environ.get("STRING_SESSION", None) # Telethon Based String Session (2nd ID) [ From https://repl.it/@SpEcHiDe/GenerateStringSession ]
    APP_ID = os.environ.get("APP_ID", None) # 2nd ID 
    APP_HASH = os.environ.get("APP_HASH", None) # 2nd ID
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", True) # Heroku App Name 
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", True) # Heroku API [From https://dashboard.heroku.com/account]
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", True)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True) # Don't Change
    BOT_NAME = os.environ.get("BOT_NAME", True) # Name Of your Bot.4
    MONGO_DB = "Rem"
    ARQ_API_URL = "https://thearq.tech"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    BOT_API_URL = os.environ.get('BOT_API_URL', "https://api.telegram.org/bot")

    HELP_IMG = os.environ.get("HELP_IMG", True)
    GROUP_START_IMG = os.environ.get("GROUP_START_IMG", True)
    REM_PHOTO = os.environ.get("REM_PHOTO", True)
    SUDO_USERS = DRAGONS 
    MONGO_DB_URI = MONGO_DB_URL
    Co_Owner_ID = 1615607413
    
    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    from TG_ROBOT.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")
      

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Config.MONGO_DB_URI
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    BOT_ID = Config.BOT_ID
    VIRUS_API_KEY = Config.VIRUS_API_KEY
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    INFOPIC = Config.INFOPIC
    REDIS_URL = Config.REDIS_URL
    BOT_USERNAME = Config.BOT_USERNAME
    STRING_SESSION = Config.STRING_SESSION
    #APP_IDX = Config.APP_IDX
    #APP_HASHX = Config.APP_HASHX
    
    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")
        

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(ALONE_ID)
DEV_USERS.add(Co_Owner_ID)
DRAGONS.add(Co_Owner_ID)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("[REM]: Connecting To Yūki • Data Center • Mumbai • Redis Database")

except BaseException:

    raise Exception("[REM ERROR]: Your Yūki • Data Center • Mumbai • Redis Database Is Not Alive, Please Check Again.")

finally:

   REDIS.ping()

   LOGGER.info("[REM]: Connection To The Aogiri • Data Center • Mumbai • Redis Database Established Successfully!")
    

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("[REM ERROR]: SpamWatch API key Is Missing! Recheck Your Config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("[REM ERROR]: Can't connect to SpamWatch!")


# Credits Logger
print("[REM] REM Is Starting. | Yūki • Black Knights Union Project | Licensed Under GPLv3.")
print("[REM] Cutie Cutie! Successfully Connected With A  Yūki • Data Center • Mumbai")
print("[REM] Project Maintained By: github.com/Awesome-RJ (t.me/Awesome_Rj)")


print("[REM]: Telegraph Installing")
telegraph = Telegraph()
print("[REM]: Telegraph Account Creating")
telegraph.create_account(short_name='REM')
updater = tg.Updater(token=TOKEN, base_url=BOT_API_URL, workers=WORKERS, request_kwargs={"read_timeout": 10, "connect_timeout": 10}, use_context=True)           
print("[REM]: TELETHON CLIENT STARTING")
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
pbot = Client("makimapbot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
print("Rem Ubot")
dispatcher = updater.dispatcher
print("[REM]: PYROGRAM CLIENT STARTING")
session_name = TOKEN.split(":")[0]
pgram = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)
print("[REM]: Connecting To Yūki • Data Center • Mumbai • MongoDB Database")
mongodb = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ("https://thearq.tech", "YIECCC-NAJARO-OLLREW-SJSRIP-ARQ", aiohttpsession)
print("[REM]: Connecting To Yūki • Data Center • Mumbai • PostgreSQL Database")
ubot = TelegramClient(StringSession(STRING_SESSION), APP_ID, APP_HASH)
print("[REM]: Connecting To Yūki • REM Userbot (t.me/Awesome_REM)")
timeout = httpx.Timeout(40)
http = httpx.AsyncClient(http2=True, timeout=timeout)

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client

apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from TG_ROBOT.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
