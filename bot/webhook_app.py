import os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

from .config import Config
from .store import init_db
from .middlewares import ConfigMiddleware
from .handlers import router as mod_router
from .scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

config = Config()
bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
dp.message.middleware(ConfigMiddleware(config))
dp.chat_member.middleware(ConfigMiddleware(config))
dp.include_router(mod_router)

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "changeme")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"

@app.on_event("startup")
async def on_startup():
    if not config.bot_token or not config.group_id:
        raise RuntimeError("Please set BOT_TOKEN and GROUP_ID in .env")
    await init_db()

    # start daily scheduler in webhook mode
    setup_scheduler(None, bot, config)

    webhook_base = os.getenv("EXTERNAL_BASE_URL")
    if not webhook_base:
        logging.warning("EXTERNAL_BASE_URL not set; skipping webhook set.")
        return
    url = webhook_base.rstrip("/") + WEBHOOK_PATH
    await bot.set_webhook(url, drop_pending_updates=True)
    logging.info(f"Webhook set to {url}")

@app.on_event("shutdown")
async def on_shutdown():
    try:
        await bot.delete_webhook()
    except Exception:
        pass

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    if request.headers.get("content-type") != "application/json":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")
    update = types.Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return JSONResponse({"ok": True})
