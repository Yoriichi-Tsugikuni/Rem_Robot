from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from TG_ROBOT import SUPPORT_CHAT, BOT_USERNAME


HELP_MSG = "Click the button below to get help manu in your pm."
START_MSG = "I'm awake already!\n<b>Haven't slept since:</b> <code>{}</code>"

PM_START_TEXT = """
────「 [{}](https://telegra.ph/file/0f9ea77c82c47bcf80c71.jpg) 」────
*Hola! {},*
✧ *ᴍʏ ɴᴀᴍᴇ ɪs `ʀᴇᴍ` ᴀ ᴄᴜᴛᴇ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ* ✧
➖➖➖➖➖➖➖➖➖➖➖➖➖
• *Uptime:* `{}`
• `{}` *users, across* `{}` *chats.*
➖➖➖➖➖➖➖➖➖➖➖➖➖
➛ Try The Help Buttons Below To Know My Abilities ××

ᴘᴏᴡᴇʀᴇᴅ ʙʏ @AogiriNetwork
"""

GROUP_START_TEXT = """
I'm awake already!
Haven't slept since: {}
"""

buttons = [

    [
        InlineKeyboardButton(text="ꜱᴜᴍᴍᴏɴ ᴍᴇ",url=f"t.me/{BOT_USERNAME}?startgroup=true"),
    ],

    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/Rem_updates"),
        InlineKeyboardButton(text="ᴅᴇᴍᴏɪᴄ ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],

    [
        InlineKeyboardButton(text="ᴅᴇᴍᴏɴꜱ ʟᴏɢꜱ", url="https://t.me/Rem_logs" ),
        InlineKeyboardButton(text="ɢʀᴏᴜᴘ", url=f"https://t.me/AnimeChatFolks"),
    ],

  [   
      InlineKeyboardButton(text="❕ꜱᴘɪʀɪᴛ ᴀʀᴛꜱ❕", callback_data="help_back") , 
    ],

]

HELP_STRINGS = """
*Main* commands available:
 ➛ /help: PM's you this message.
 ➛ /help <module name>: PM's you info about that module.
 ➛ /donate: information on how to donate!
 ➛ /settings:
   ❂ in PM: will send you your settings for all supported modules.
   ❂ in a group: will redirect you to pm, with all that chat's settings.
"""

DONATE_STRING = """❂ I'm Free for Everyone ❂"""

