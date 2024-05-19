from telegram import Update
from telegram.ext import ContextTypes
from misc import show_interaction, random_catch_phrase, get_message_text


def reply_bot(user, text):
    return random_catch_phrase(user, text)


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply to the user message."""
    # write the username and the message in the log
    user = update.effective_user
    # message = update.message.text  # todo
    text = reply_bot(user, get_message_text(update))
    show_interaction(update, text)
    await update.message.reply_text(text)
