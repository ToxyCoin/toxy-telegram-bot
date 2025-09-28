import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import Config
from .store import init_db
from .middlewares import ConfigMiddleware
from .scheduler import setup_scheduler
from .handlers import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

async def main():
    config = Config()
    if not config.bot_token or not config.group_id:
        raise RuntimeError("Please set BOT_TOKEN and GROUP_ID in .env")

    await init_db()

    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()
    dp.message.middleware(ConfigMiddleware(config))
    dp.chat_member.middleware(ConfigMiddleware(config))
    dp.include_router(router)

    setup_scheduler(dp, bot, config)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
