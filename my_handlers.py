"""
Define a few command handlers. These usually take the two arguments update and context.
"""
from telegram import ForceReply, Update
from telegram.ext import ContextTypes
import numpy as np
from time import gmtime, strftime
from architect import Architect
from my_reply import show_interaction


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    Architect().add_user(user.id, user.username)
    text = f"Ciao {user.mention_html()}! Sono Omar2.0, il tuo assistente personale. Dimmi cosa posso fare per te!"
    show_interaction(update, text)
    await update.message.reply_html(text, reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = "Commands: /statr, /help, /users, /babbo_natale_segreto"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def babbo_natale_segreto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /babbo_natale_segreto is issued."""
    users = Architect().get_users()
    user_names = list(users.values())
    this_user = update.effective_user.username
    text = "Babbo Natale Segreto!\n\n"
    text += f"Utenti registrati ({len(user_names)}):\n"
    text += '\n'.join(list(users.values()))
    text += '\n(Assicurati che ci siate tutti!!)\n\n'
    year = strftime("%Y", gmtime())
    text += f'Il tuo babbo natale segreto {year} è '
    text += babbo_natale(user_names)[this_user]
    text += '!'
    show_interaction(update, text)
    await update.message.reply_text(text)


async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /users is issued."""
    users = Architect().get_users()
    text = "Utenti registrati: "
    text += ', '.join(list(users.values()))
    show_interaction(update, text)
    await update.message.reply_text(text)


def pick_random_gift_receivers(n, seed):
    np.random.seed(seed)
    v = list(np.random.permutation(n))
    return [v[v.index(i)-1] for i in range(n)]


def babbo_natale(names: list) -> dict:
    names = np.array(names)
    year = strftime("%Y", gmtime())
    indices = pick_random_gift_receivers(len(names), int(year))
    receivers = {names[i]: names[j] for i, j in enumerate(indices)}
    return receivers
