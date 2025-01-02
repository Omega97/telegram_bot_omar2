from telegram import Update
from telegram.ext import ContextTypes
from scripts.utils import show_interaction, get_message_text, get_user_full_name, moderate


def reply_bot(user, text: str, user_id) -> str:
    """reply with the last message written by another user"""
    username = get_user_full_name(user)
    username = username.split(' ')[0]
    answer = f'Ciao {username}! Do you need /help?'
    return answer


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply to the user message"""
    user = update.effective_user
    message_text = get_message_text(update)

    if not hasattr(update.message, 'reply_text'):
        # if the user edits an old message, it registers as a None message
        pass
    else:
        user_id = user.id
        reply_text = reply_bot(user, message_text, user_id)
        show_interaction(update, reply_text)
        await update.message.reply_text(reply_text)
