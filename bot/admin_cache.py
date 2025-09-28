import time
from typing import Dict, List
from aiogram import Bot

class AdminCache:
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self.cache: Dict[int, tuple[float, list[int]]] = {}

    async def get_admin_ids(self, bot: Bot, chat_id: int) -> List[int]:
        now = time.time()
        if chat_id in self.cache:
            ts, ids = self.cache[chat_id]
            if now - ts < self.ttl:
                return ids

        admins = await bot.get_chat_administrators(chat_id)
        ids = [a.user.id for a in admins]
        self.cache[chat_id] = (now, ids)
        return ids
