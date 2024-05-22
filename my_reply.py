from telegram import Update
from telegram.ext import ContextTypes
from misc import show_interaction, get_message_text, get_user_full_name
from architect import Architect


def reply_bot(user, text: str, user_id) -> str:
    """reply with the last message written by another user"""
    architect = Architect()
    old_id, old_message = architect.get_last_user_message()
    architect.set_last_user_message(user_id, text)
    if old_id != user_id and old_message is not None:
        # send the old message
        return old_message
    else:
        # standard reply
        username = get_user_full_name(user)
        return f'Ciao {username}!'


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply to the user message"""
    user = update.effective_user
    text = get_message_text(update)
    user_id = user.id
    text = reply_bot(user, text, user_id)
    show_interaction(update, text)
    await update.message.reply_text(text)
