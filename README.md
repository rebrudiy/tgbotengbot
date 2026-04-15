# engimprover

> vibecoded in 5 minutes, no brain cells used

Telegram bot that roasts your English and tells you how to fix it.

## What it does

Drop it in your group chat. Reply to any message with `/check` or tag the bot — it reviews the English and gives feedback. Toxic by default.

## Commands

| Command | What it does |
|---|---|
| `/check [text]` | Check inline text or reply to a message |
| `/mode [name]` | Switch tone: `friendly`, `formal`, `toxic`, `teacher`, `chill` |
| `/length [name]` | Switch length: `short`, `medium`, `detailed` |
| `/settings` | See your current settings |
| `/modes` | List all modes |

## Setup

```bash
git clone https://github.com/rebrudiy/tgbotengbot.git
cd tgbotengbot
cp .env.example .env
nano .env  # fill in your tokens
docker compose up -d
```

## .env

```
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
OWNER_ID=your_telegram_user_id
```

## Stack

- Python 3.11
- python-telegram-bot v20+
- Claude API (Haiku)
- Docker
