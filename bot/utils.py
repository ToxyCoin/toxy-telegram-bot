import re
from typing import Iterable

URL_REGEX = re.compile(
    r'(?i)\b((?:https?://|www\.|t\.me/)[^\s]+|\b[\w-]+\.(?:com|net|org|io|co|xyz|app|site|link|info|me)\b)'
)

AD_KEYWORDS = [
    "free crypto",
    "vip signals",
    "airdrop now",
    "pump and dump",
    "quick profit",
    "easy money",
    "betting",
    "casino",
    "xxx",
    "porn",
    "loan approval",
    "make $",
    "join my channel",
    "promo code",
    "discount here",
    "click here",
]

def contains_link(text: str) -> bool:
    return bool(URL_REGEX.search(text or ""))

def contains_advert(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    for kw in AD_KEYWORDS:
        if kw in t:
            return True
    return False

def mention(user) -> str:
    name = user.full_name or "there"
    return f"[{name}](tg://user?id={user.id})"

def is_admin_id(user_id: int, admin_ids: Iterable[int]) -> bool:
    return user_id in set(admin_ids)
