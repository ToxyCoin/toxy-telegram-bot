# Telegram Moderation Bot — Webhook (Render Free)

This repo is ready for **Render Free Web Service** (webhook mode). No local PC needed.

## What it does
- Deletes spam (>=3 msgs / 30s), links, ad keywords
- Welcomes new members
- /help, /rules, /ping
- Daily messages at 09:00 and 22:00 (Europe/Istanbul)
- Admins are exempt

## Deploy on Render (Free)
1. Push this project to a **GitHub** repo.
2. Go to **https://render.com** → **New +** → **Web Service** → connect the repo.
3. It detects the **Dockerfile** (kept simple). Create the service.
4. In **Environment** tab, add the variables from `.env` (you can paste whole content key-by-key).
   - BOT_TOKEN
   - GROUP_ID
   - TIMEZONE, GOOD_MORNING_TIME, GOOD_EVENING_TIME
   - WELCOME_MESSAGE, HELP_REPLY, GOOD_MORNING_TEXT, GOOD_EVENING_TEXT
   - EXTRA_ADMIN_IDS (optional)
   - WEBHOOK_SECRET  (already included here)
5. After the service is created, Render gives a URL like `https://your-app.onrender.com`.
   - Set **EXTERNAL_BASE_URL** to that URL and **Save & Restart**.
6. Add the bot to your Telegram group and **Promote to Admin** (Delete/Restrict permissions).
7. Test `/ping` (should respond `pong`). Links and spam should be moderated automatically.

## Local test (optional)
```bash
pip install -r requirements.txt
uvicorn bot.webhook_app:app --reload
```
Then set `EXTERNAL_BASE_URL` to your public tunnel (e.g., Cloudflare Tunnel/Ngrok) and restart so webhook can be set.

## Notes
- The app sets Telegram webhook on startup if `EXTERNAL_BASE_URL` is present.
- Scheduler for daily messages is enabled in webhook mode as well.
- SQLite state at `data/state.db` is ephemeral on Render Free (use paid persistent storage if you need long-term logs).
