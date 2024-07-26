from telegram import Update
from telegram.ext import ContextTypes
from random import shuffle
from scripts.utils import show_interaction, get_message_text, get_user_full_name, moderate
from architect import Architect


def reply_bot(user, text: str, user_id, n_lest_messages=100, n_write=3) -> str:
    """reply with the last message written by another user"""
    architect = Architect()
    user_messages = architect.get_user_messages()

    if len(user_messages):
        # return the last message
        user_messages = user_messages[-n_lest_messages:]
        user_messages = [message.lower() for message in user_messages]
        user_messages = list(set(user_messages))

        shuffle(user_messages)
        user_messages = user_messages[:n_write]

        answer = ' - '.join(user_messages)

        text = moderate(text)
        architect.save_user_message(text)

        return answer
    else:
        # standard reply
        username = get_user_full_name(user)
        answer = f'Ciao {username}!'
        return answer


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply to the user message"""

    # for key in dir(update):
    #     a = getattr(update, key)
    #     if a is None:
    #         continue
    #     text = str(a)
    #     print(f'\n\033[94m{key}\033[0m {text}')

    user = update.effective_user
    text = get_message_text(update)
    user_id = user.id
    text = reply_bot(user, text, user_id)
    show_interaction(update, text)
    await update.message.reply_text(text)
