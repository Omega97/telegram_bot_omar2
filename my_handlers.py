"""
Define a few command handlers.
These usually take the two arguments update and context.
"""
from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from time import gmtime, strftime
from architect import Architect
from my_reply import show_interaction
from misc import get_user_full_name, babbo_natale


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    usern_full_name = get_user_full_name(user)

    print(update.effective_user)
    print(f">>> {usern_full_name} ha scritto /start")

    Architect().add_user(user.id, usern_full_name)
    text = f"Ciao {user.mention_html()}! " \
           f"Sono Omar2.0, il tuo assistente personale 🤖\n" \
           f"Dimmi cosa posso fare per te! 😺\n" \
           f"Scrivi /help per vedere i comandi disponibili 📚"
    show_interaction(update, text)
    await update.message.reply_html(text, reply_markup=ForceReply(selective=True))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = "Commands: /start, /help, /users, /babbo_natale_segreto, /burp, /random_user"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def babbo_natale_segreto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /babbo_natale_segreto is issued."""
    user_names = Architect().get_user_names()

    this_user = get_user_full_name(update.effective_user)

    text = "🎄🎄🎄☃❄ Babbo Natale Segreto! 🎅🎁🎄🎄🎄\n\n"
    text += f"Utenti registrati: {len(user_names)} (Assicurati che ci siate tutti!!!)\n"

    for name in user_names:
        text += f'- {name}\n'

    text += '\n'
    year = strftime("%Y", gmtime())
    text += f'Il tuo Babbo Natale segreto {year} è ➡{babbo_natale(user_names)[this_user]}⬅ !'
    show_interaction(update, text)
    await update.message.reply_text(text)


async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /users is issued."""
    users = Architect().get_user_names()
    text = "👥 Utenti registrati: "
    text += ', '.join(list(users))
    show_interaction(update, text)
    await update.message.reply_text(text)


async def burp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /burp is issued."""
    text = "Ma Omar!"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def random_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /random_user is issued."""
    user_names = Architect().get_user_names()
    text = f"👥 Utenti registrati: {len(user_names)}\n"
    text += f"👤 Utente casuale: {user_names.pop()}"
    show_interaction(update, text)
    await update.message.reply_text(text)
