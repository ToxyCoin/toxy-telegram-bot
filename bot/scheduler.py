import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def parse_hhmm(s: str) -> tuple[int,int]:
    parts = s.strip().split(":")
    h = int(parts[0]); m = int(parts[1]) if len(parts) > 1 else 0
    return h, m

def setup_scheduler(dp, bot, config):
    tz = pytz.timezone(config.timezone)
    scheduler = AsyncIOScheduler(timezone=tz)

    gm_h, gm_m = parse_hhmm(config.gm_time)
    ge_h, ge_m = parse_hhmm(config.ge_time)

    async def send_gm():
        await bot.send_message(chat_id=config.group_id, text=config.gm_text)

    async def send_ge():
        await bot.send_message(chat_id=config.group_id, text=config.ge_text)

    scheduler.add_job(send_gm, "cron", hour=gm_h, minute=gm_m, id="good_morning")
    scheduler.add_job(send_ge, "cron", hour=ge_h, minute=ge_m, id="good_evening")
    scheduler.start()
    return scheduler
