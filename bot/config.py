from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    group_id: int = int(os.getenv("GROUP_ID", "0"))
    timezone: str = os.getenv("TIMEZONE", "Europe/Istanbul")
    gm_time: str = os.getenv("GOOD_MORNING_TIME", "09:00")
    ge_time: str = os.getenv("GOOD_EVENING_TIME", "22:00")
    welcome_message: str = os.getenv("WELCOME_MESSAGE", "Welcome {mention}! Please read the rules with /rules")
    help_reply: str = os.getenv("HELP_REPLY", "An admin will contact you shortly.")
    gm_text: str = os.getenv("GOOD_MORNING_TEXT", "Good morning ☀️")
    ge_text: str = os.getenv("GOOD_EVENING_TEXT", "Good evening 🌙")
    extra_admin_ids: list[int] | None = None

    def __post_init__(self):
        extra = os.getenv("EXTRA_ADMIN_IDS", "").strip()
        if extra:
            self.extra_admin_ids = [int(x) for x in extra.split(",") if x.strip().isdigit()]
        else:
            self.extra_admin_ids = []
