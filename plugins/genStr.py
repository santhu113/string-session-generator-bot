import os
import json
import time
import asyncio

from asyncio.exceptions import TimeoutError

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

Santhuvcplayerbot_IMG = "https://te.legra.ph/file/422292c9fb5561a9be9c6.jpg"
PM_START_TEXT = """
*👋 Hello {} !*

🔥 ɪᴀᴍ ᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ. 

✗ *Pᴏᴡᴇʀᴇᴅ 💕 Bʏ: 𝙼𝚄𝚂𝙸𝙲 𝙽𝙴𝚃𝚆𝙾𝚁𝙺!*

ғᴏʀ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴛʀɪɴɢ sᴇssɪᴏɴ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ `ᴀᴘɪ_ɪᴅ` 💞
"""
────────────────────── 

HASH_TEXT = "ᴏᴋ ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ `ᴀᴘɪ_ʜᴀsʜ` ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\n\nᴘʀᴇss /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ.🐧"
PHONE_NUMBER_TEXT = (
    "📞__ ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ"
    "ɪɴᴄʟᴜᴅᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ.__\n**ᴇɢ:** `+917981630016`\n\n"
    "ᴘʀᴇss /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."
)



@Client.on_message(filters.private & filters.command("start"))
async def generate_str(c, m):
    get_api_id = await c.ask(
        chat_id=m.chat.id,
        text=API_TEXT.format(m.from_user.mention(style='md')),
        filters=filters.text
    )
    api_id = get_api_id.text
    if await is_cancel(m, api_id):
        return

    await get_api_id.delete()
    await get_api_id.request.delete()
    try:
        check_api = int(api_id)
    except Exception:
        await m.reply("**--😅 ᴀᴘɪ ɪᴅ ɪɴᴠᴀʟɪᴅ 💞--**\nPʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return

    get_api_hash = await c.ask(
        chat_id=m.chat.id, 
        text=HASH_TEXT,
        filters=filters.text
    )
    api_hash = get_api_hash.text
    if await is_cancel(m, api_hash):
        return

    await get_api_hash.delete()
    await get_api_hash.request.delete()

    if not len(api_hash) >= 30:
        await m.reply("--**☺ ᴀᴘɪ ʜᴀsʜ ɪɴᴠᴀʟɪᴅ 💞**--\nᴘʀᴇss /start to create again.")
        return

    try:
        client = Client(":memory:", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await c.send_message(m.chat.id ,f"**☹️ ᴇʀʀᴏʀ: ☹️** `{str(e)}`\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return

    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    while True:
        get_phone_number = await c.ask(
            chat_id=m.chat.id,
            text=PHONE_NUMBER_TEXT
        )
        phone_number = get_phone_number.text
        if await is_cancel(m, phone_number):
            return
        await get_phone_number.delete()
        await get_phone_number.request.delete()

        confirm = await c.ask(
            chat_id=m.chat.id,
            text=f'🤔 ɪs `{phone_number}` ᴄᴏʀʀᴇᴄᴛ? (y/n): \n\nᴛʏᴘᴇ: `y` (ɪғ ʏᴇs)\nᴛʏᴘᴇ: `n` (ɪғ ɴᴏ)'
        )
        if await is_cancel(m, confirm.text):
            return
        if "y" in confirm.text.lower():
            await confirm.delete()
            await confirm.request.delete()
            break
    try:
        code = await client.send_code(phone_number)
        await asyncio.sleep(1)
    except FloodWait as e:
        await m.reply(f"__sᴏʀʀʏ ᴛᴏ sᴀʏ ʏᴏᴜ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ ғʟᴏᴏᴅᴡᴀɪᴛ ᴏғ {e.x} sᴇᴄᴏɴᴅs 😞__")
        return
    except ApiIdInvalid:
        await m.reply("🕵‍♂ ᴛʜᴇ ᴀᴘɪ ɪᴅ ᴏʀ ᴀᴘɪ ʜᴀsʜ ɪs ɪɴᴠᴀʟɪᴅ.\n\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return
    except PhoneNumberInvalid:
        await m.reply("☎ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪs ɪɴᴠᴀʟɪᴅ.`\n\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return

    try:
        sent_type = {"app": "ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘᴘ 💌",
            "sms": "sᴍs 💬",
            "call": "ᴘʜᴏɴᴇ ᴄᴀʟʟ 📱",
            "flash_call": "ᴘʜᴏɴᴇ ғʟᴀsʜ ᴄᴀʟʟ 📲"
        }[code.type]
        otp = await c.ask(
            chat_id=m.chat.id,
            text=(f"ɪ ʜᴀᴅ sᴇɴᴛ ᴀɴ ᴏᴛᴘ ᴛᴏ ᴛʜᴇ ɴᴜᴍʙᴇʀ `{phone_number}` ᴛʜʀᴏᴜɢʜ {sent_type}\n\n"
                  "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ `𝟷 𝟸 𝟹 𝟺 𝟻` __(ᴘʀᴏᴠɪᴇᴅ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ʙᴇᴛᴡᴇᴇɴ ɴᴜᴍʙᴇʀs)__\n\n"
                  "ɪғ ʙᴏᴛ ɴᴏᴛ sᴇɴᴅɪɴɢ ᴏᴛᴘ ᴛʜᴇɴ ᴛʀʏ /start ᴛʜᴇ ʙᴏᴛ.\n"
                  "ᴘʀᴇss /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ."), timeout=300)
    except TimeoutError:
        await m.reply("**⏰ ᴛɪᴍᴇᴏᴜᴛ ᴇʀʀᴏʀ:** ʏᴏᴜ ʀᴇᴀᴄʜᴇᴅ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴏғ 𝟻 ᴍɪɴ.\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return
    if await is_cancel(m, otp.text):
        return
    otp_code = otp.text
    await otp.delete()
    await otp.request.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await m.reply("**😡 ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ**\n\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return 
    except PhoneCodeExpired:
        await m.reply("**🔥 ᴄᴏᴅᴇ ɪs ᴇxᴘɪʀᴇᴅ**\n\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await c.ask(
                chat_id=m.chat.id, 
                text="`🔐 𝚃𝚑𝚒𝚜 𝚊𝚌𝚌𝚘𝚞𝚗𝚝 𝚑𝚊𝚟𝚎 𝚝𝚠𝚘-𝚜𝚝𝚎𝚙 𝚟𝚎𝚛𝚒𝚏𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚌𝚘𝚍𝚎.\n𝙿𝚕𝚎𝚊𝚜𝚎 𝚎𝚗𝚝𝚎𝚛 𝚢𝚘𝚞𝚛 𝚜𝚎𝚌𝚘𝚗𝚍 𝚏𝚊𝚌𝚝𝚘𝚛 𝚊𝚞𝚝𝚑𝚎𝚗𝚝𝚒𝚌𝚊𝚝𝚒𝚘𝚗 𝚌𝚘𝚍𝚎.`\n𝙿𝚛𝚎𝚜𝚜 /cancel 𝚝𝚘 𝙲𝚊𝚗𝚌𝚎𝚕.",
                timeout=300
            )
        except TimeoutError:
            await m.reply("**⏰ ᴛɪᴍᴇᴏᴜᴛ ᴇʀʀᴏʀ:** ʏᴏᴜ ʀᴇᴀᴄʜᴇᴅ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴏғ 𝟻 ᴍɪɴ.\nᴘʀᴇss /start ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ.")
            return
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        await two_step_code.delete()
        await two_step_code.request.delete()
        try:
            await client.check_password(new_code)
        except Exception as e:
            await m.reply(f"**⚠️ ᴇʀʀᴏʀ:** `{str(e)}`")
            return
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ ᴇʀʀᴏʀ:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", f"**ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ 👇**\n\n`{session_string}`\n\nᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ {(await c.get_me()).mention(style='md')}")
        text = "💘 sᴜᴄᴄᴇssғᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ ᴀɴᴅ sᴇɴᴛ ᴛᴏ ʏᴏᴜ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.\nᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ᴏʀ ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ʏᴏᴜʀ sᴇssɪᴏɴ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
        )
        await c.send_message(m.chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ ᴇʀʀᴏʀ:** `{str(e)}`")
        return
    try:
        await client.stop()
    except:
        pass


@Client.on_message(filters.private & filters.command("help"))
async def help(c, m):
    await help_cb(c, m, cb=False)


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m, cb=True):
    help_text = """**ʜᴇʏ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ??👨‍✈️**


🏹 ᴘʀᴇss ᴛʜᴇ sᴛᴀʀᴛ ʙᴜᴛᴛᴏɴ

⚔️ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ_ɪᴅ ᴡʜᴇɴ ʙᴏᴛ ᴀsᴋ.

🔰 ᴛʜᴇɴ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ_ʜᴀsʜ ᴡʜᴇɴ ʙᴏᴛ ᴀsᴋ.

❤ sᴇɴᴅ ʏᴏᴜʀ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ.

💓 sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ ʀᴇᴄɪᴠᴇᴠᴇᴅ ᴛᴏ ʏᴏᴜʀ ɴᴜᴍᴇʀ ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ `𝟷 𝟸 𝟹 𝟺 𝟻` (ɢɪᴠᴇ sᴘᴀᴄᴇ ʙ/ᴡ ᴇᴀᴄʜ ᴅɪɢɪᴛ)

🔥 (ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ sᴇɴᴅ ᴛᴏ ʙᴏᴛ ɪғ ʙᴏᴛ ᴀsᴋ.)


**ɴᴏᴛᴇ:**

ɪғ ʏᴏᴜ ᴍᴀᴅᴇ ᴀɴʏ ᴍɪsᴛᴀᴋᴇ ᴀɴʏᴡʜᴇʀᴇ ᴘʀᴇss /cancel ᴀɴᴅ ᴛʜᴇɴ ᴘʀᴇss /start
"""

    buttons = [[
        InlineKeyboardButton('🔰 ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('🗑 ʙɪɴ', callback_data='close')
    ]]
    if cb:
        await m.answer()
        await m.message.edit(text=help_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(text=help_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)


@Client.on_message(filters.private & filters.command("about"))
async def about(c, m):
    await about_cb(c, m, cb=False)


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m, cb=True):
    me = await c.get_me()
    about_text = f"""**ᴍʏ ᴅᴇᴛᴀɪʟs:**

__❣️ ᴍʏ ɴᴀᴍᴇ:__ {me.mention(style='md')}
    
__💝 ʟᴀɴɢᴜᴀɢᴇ:__ [ᴘʏᴛʜᴏɴ𝟹](https://www.python.org/)

__💗 ғʀᴀᴍᴇᴡᴏʀᴋ:__ [ᴘʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)

__💓 ᴅᴇᴠᴇʟᴏᴘᴇʀ:__ [ᴍᴜsɪᴄ ɢʀᴏᴜᴘ](https://t.me/musicupdates12)

__💖 ᴄʜᴀɴɴᴇʟ:__ [ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs](https://t.me/santhubotupadates)

__💔 ɢʀᴏᴜᴘ:__ [sᴀɴᴛʜᴜ ʙᴏᴛ sᴜᴘᴘᴏʀᴛ](https://t.me/musicupdates12)

__💕 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ:__ [ʀᴇᴘᴏ](http://t.me/musicupdates12)

__💘 ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ:__ [sᴀɴᴛʜᴜ ʙᴏᴛs](https://youtube.com/channel/UC7QMr8IDR65vciXrwx4XLiQ)
"""

    buttons = [[
        InlineKeyboardButton('❣️ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('🗑 ʙɪɴ', callback_data='close'), 
    ]]
    if cb:
        await m.answer()
        await m.message.edit(about_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(about_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)


@Client.on_callback_query(filters.regex('^close$'))
async def close(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("❌ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return True
    return False
