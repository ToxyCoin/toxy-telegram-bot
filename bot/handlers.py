import asyncio
from typing import Dict, Deque
from collections import defaultdict, deque

from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command
from aiogram.enums.chat_member_status import ChatMemberStatus

from .utils import contains_link, contains_advert, mention
from .store import add_warn
from .admin_cache import AdminCache

router = Router()

message_windows: Dict[int, Dict[int, Deque[float]]] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=10)))
SPAM_WINDOW_SEC = 30
SPAM_THRESHOLD = 3

admin_cache = AdminCache(ttl_seconds=600)

async def is_admin(message: Message, extra_admin_ids: list[int]) -> bool:
    admins = await admin_cache.get_admin_ids(message.bot, message.chat.id)
    admin_ids = set(admins) | set(extra_admin_ids or [])
    return message.from_user.id in admin_ids

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! I'm a moderation bot. Add me to a group and grant admin rights. Use /help for info.")

@router.message(Command("help"))
async def cmd_help(message: Message, config):
    await message.answer(config.help_reply)

@router.message(Command("rules"))
async def cmd_rules(message: Message):
    try:
        with open("data/rules.txt", "r", encoding="utf-8") as f:
            rules = f.read()
    except Exception:
        rules = "Rules are not set yet."
    await message.answer(rules)

@router.message(Command("ping"))
async def cmd_ping(message: Message):
    await message.answer("pong")

@router.chat_member()
async def on_user_join(event: ChatMemberUpdated, config):
    if event.chat.id != config.group_id:
        return
    if event.new_chat_member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED):
        user = event.new_chat_member.user
        text = config.welcome_message.format(mention=mention(user))
        await event.bot.send_message(chat_id=event.chat.id, text=text, parse_mode="Markdown")

@router.message(F.chat.type.in_({"group", "supergroup"}))
async def moderate(message: Message, config):
    if message.chat.id != config.group_id:
        return
    if not message.from_user or message.from_user.is_bot:
        return
    if await is_admin(message, config.extra_admin_ids):
        return

    text = message.text or message.caption or ""

    dq = message_windows[message.chat.id][message.from_user.id]
    now = message.date.timestamp()
    dq.append(now)
    while dq and now - dq[0] > SPAM_WINDOW_SEC:
        dq.popleft()
    if len(dq) >= SPAM_THRESHOLD:
        try:
            await message.delete()
        except Exception:
            pass
        warns = await add_warn(message.chat.id, message.from_user.id, 1)
        await message.answer(
            f"{mention(message.from_user)} please avoid spamming. (warning #{warns})",
            parse_mode="Markdown",
            reply_to_message_id=message.message_id if message.message_id else None
        )
        return

    if text and contains_link(text):
        try:
            await message.delete()
        except Exception:
            pass
        warns = await add_warn(message.chat.id, message.from_user.id, 1)
        await message.answer(f"{mention(message.from_user)} links are not allowed.", parse_mode="Markdown")
        return

    if text and contains_advert(text):
        try:
            await message.delete()
        except Exception:
            pass
        warns = await add_warn(message.chat.id, message.from_user.id, 1)
        await message.answer(f"{mention(message.from_user)} advertising is not allowed.", parse_mode="Markdown")
        return
