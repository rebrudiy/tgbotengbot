import os
from dotenv import load_dotenv
from telegram import Update, ChatMemberUpdated
from telegram.ext import ContextTypes

from analyzer import analyze_text
from modes import MODES, LENGTHS, DEFAULT_MODE, DEFAULT_LENGTH
from user_settings import get_settings, set_mode, set_length

load_dotenv()
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


def _is_private(update: Update) -> bool:
    return update.effective_chat.type == "private"


async def handle_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Leave any group the bot was added to by someone other than the owner."""
    result: ChatMemberUpdated = update.my_chat_member
    if result.new_chat_member.status not in ("member", "administrator"):
        return
    if result.from_user.id != OWNER_ID:
        await context.bot.leave_chat(result.chat.id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_private(update):
        return
    await update.message.reply_text(
        "Hey! I'm your English reviewer.\n\n"
        "How to use me:\n"
        "• Reply to any message and tag me (@botusername) to check that message\n"
        "• /check [text] — check the text you provide\n\n"
        "Customize your experience:\n"
        "• /mode [name] — set tone (friendly, formal, toxic, teacher, chill)\n"
        "• /length [name] — set response length (short, medium, detailed)\n"
        "• /settings — show your current settings\n"
        "• /modes — list all available modes"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_private(update):
        return
    text = " ".join(context.args).strip() if context.args else ""

    # If no inline text, check if it's a reply to a message
    if not text and update.message.reply_to_message:
        if not update.message.reply_to_message.text:
            await update.message.reply_text("I can only check text messages, not photos or files.")
            return
        text = update.message.reply_to_message.text

    if not text:
        await update.message.reply_text("Please provide text to check. Example: /check Hello, how are you?")
        return

    settings = get_settings(update.effective_user.id)
    await _send_analysis(update, text, settings["mode"], settings["length"])


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_private(update):
        return
    message = update.message

    if not message.reply_to_message:
        return

    if not message.reply_to_message.text:
        await message.reply_text("I can only check text messages, not photos or files.")
        return

    text = message.reply_to_message.text
    settings = get_settings(update.effective_user.id)
    await _send_analysis(update, text, settings["mode"], settings["length"], reply_to=message.reply_to_message)


async def _send_analysis(update: Update, text: str, mode: str, length: str, reply_to=None) -> None:
    thinking_msg = await update.message.reply_text("Checking...", reply_to_message_id=reply_to.message_id if reply_to else None)

    try:
        result = await analyze_text(text, mode, length)
        await thinking_msg.edit_text(result)
    except Exception as e:
        print(f"API ERROR: {e}")
        await thinking_msg.edit_text("Something went wrong with the API. Try again in a moment.")


async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        modes_list = ", ".join(MODES.keys())
        await update.message.reply_text(f"Usage: /mode [name]\nAvailable: {modes_list}")
        return

    mode = context.args[0].lower()
    if mode not in MODES:
        modes_list = ", ".join(MODES.keys())
        await update.message.reply_text(f"Unknown mode '{mode}'. Available: {modes_list}")
        return

    set_mode(update.effective_user.id, mode)
    await update.message.reply_text(f"Mode set to: {mode}")


async def length_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        lengths_list = ", ".join(LENGTHS.keys())
        await update.message.reply_text(f"Usage: /length [name]\nAvailable: {lengths_list}")
        return

    length = context.args[0].lower()
    if length not in LENGTHS:
        lengths_list = ", ".join(LENGTHS.keys())
        await update.message.reply_text(f"Unknown length '{length}'. Available: {lengths_list}")
        return

    set_length(update.effective_user.id, length)
    await update.message.reply_text(f"Response length set to: {length}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings(update.effective_user.id)
    await update.message.reply_text(
        f"Your current settings:\n"
        f"Mode: {settings['mode']}\n"
        f"Length: {settings['length']}"
    )


async def modes_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["Available modes:\n"]
    for name, info in MODES.items():
        lines.append(f"{name} — {info['description']}")
    lines.append("\nAvailable lengths:\n")
    for name, info in LENGTHS.items():
        lines.append(f"{name} — {info['description']}")
    await update.message.reply_text("\n".join(lines))
