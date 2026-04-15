import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters

from handlers import (
    start,
    help_command,
    check_command,
    handle_mention,
    handle_bot_added,
    mode_command,
    length_command,
    settings_command,
    modes_command,
)

load_dotenv()


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is not set in .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CommandHandler("mode", mode_command))
    app.add_handler(CommandHandler("length", length_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("modes", modes_command))

    # Leave groups added by non-owner
    app.add_handler(ChatMemberHandler(handle_bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    # Handle replies where the bot is mentioned
    app.add_handler(MessageHandler(filters.REPLY & filters.Entity("mention"), handle_mention))

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
