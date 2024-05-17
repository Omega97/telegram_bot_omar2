from telegram import Update
from telegram.ext import ContextTypes


def show_interaction(update, reply):
    username = update.effective_user.username
    user_message = update.message.text
    print(f"{username}: {user_message}")
    print(f">>> {reply}")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply to the user message."""
    # write the username and the message in the log
    text = update.message.text + '?'
    show_interaction(update, text)
    await update.message.reply_text(text)
