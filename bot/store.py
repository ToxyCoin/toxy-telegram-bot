import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "state.db")

INIT_SQL = '''
CREATE TABLE IF NOT EXISTS warns (
    chat_id INTEGER,
    user_id INTEGER,
    warns INTEGER DEFAULT 0,
    PRIMARY KEY (chat_id, user_id)
);
CREATE TABLE IF NOT EXISTS kv (
    key TEXT PRIMARY KEY,
    value TEXT
);
'''

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(INIT_SQL)
        await db.commit()

async def get_warns(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT warns FROM warns WHERE chat_id=? AND user_id=?", (chat_id, user_id))
        row = await cur.fetchone()
        return row[0] if row else 0

async def add_warn(chat_id: int, user_id: int, inc: int = 1) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO warns(chat_id,user_id,warns) VALUES(?,?,COALESCE(?,0)) "
            "ON CONFLICT(chat_id,user_id) DO UPDATE SET warns=warns+excluded.warns",
            (chat_id, user_id, inc),
        )
        await db.commit()
        return await get_warns(chat_id, user_id)

async def kv_set(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO kv(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
        await db.commit()

async def kv_get(key: str) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT value FROM kv WHERE key=?", (key,))
        row = await cur.fetchone()
        return row[0] if row else None
