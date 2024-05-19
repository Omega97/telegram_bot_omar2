"""
Define a few command handlers.
These usually take the two arguments update and context.
"""
from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from time import time, gmtime, strftime
import numpy as np
from architect import Architect
from my_reply import show_interaction
from misc import get_user_full_name, babbo_natale
from place import Place


COMMANDS = dict()
PLACING_TILE_POINTS = 1


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    text = ("Commands: " + ", ".join(["/" + key for key in COMMANDS]) + "\n")
    show_interaction(update, text)
    await update.message.reply_text(text)


async def babbo_natale_segreto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /babbo_natale_segreto is issued."""
    architect = Architect()
    user_ids = architect.get_santas()
    user_names = [architect.get_user_name(user_id) for user_id in user_ids]

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


async def get_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /users is issued."""
    architect = Architect()
    users = [f'{architect.get_user_emoji(i)} {architect.get_user_name(i)}' for i in architect.user_info]
    text = "👥 Utenti registrati: "
    text += ', '.join(users)
    show_interaction(update, text)
    await update.message.reply_text(text)


async def burp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /burp is issued."""
    text = "Ma Omar!"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def random_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /random_user is issued."""
    architect = Architect()
    user_info = architect.get_user_info()
    random_user_id = list(user_info.keys())[np.random.randint(len(user_info))]
    emoji = architect.get_user_emoji(random_user_id)
    text = f"👥 Utenti registrati: {len(user_info)}\n"
    text += f"👤 Utente casuale: {emoji} {architect.get_user_name(random_user_id)}"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def place_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /place is issued."""
    place = Place()
    architect = Architect()
    user_id = update.effective_user.id

    args = context.args
    text = '--- Telegram Place ---\n'
    now = time()

    if len(args) >= 2:
        # coordinates
        last_place_time = architect.get_last_place_time(user_id)
        time_to_wait = 0

        if last_place_time is not None:
            time_to_wait = place.minutes_cooldown * 60 - now + last_place_time

        if time_to_wait <= 0:
            # place the pixel
            try:
                x = int(args[0])
                y = int(args[1])
                user_id = update.effective_user.id
                print(f'> effective user id: {user_id}')
                place.swap_pixel(x, y, user_id=user_id)
                architect.set_last_place_time(user_id, now)
                architect.add_place_tiles_count(user_id)
                architect.increase_points(user_id, PLACING_TILE_POINTS)
                text += str(place)
            except Exception as e:
                text = f"{e}: I valori inseriti non sono validi!"

            show_interaction(update, text)
            await update.message.reply_text(text)
        else:
            # wait
            text += f'mancano ancora {time_to_wait:.0f} secondi...\n'
            show_interaction(update, text)
            await update.message.reply_text(text)
    elif len(args) == 1:
        if args[0] == 'stats':
            # show stats

            architect = Architect()
            names, emojis, tiles = architect.get_tile_leaderboard()

            for i in range(len(names)):
                s = '' if tiles[i] == 1 else 's'
                text += f'{emojis[i]} {names[i]}: {tiles[i]} tile{s}\n'

            show_interaction(update, text)
            await update.message.reply_text(text)
    else:
        # show canvas
        text += f'Piazza un emoji ogni {place.minutes_cooldown} minuti con /place [x] [y]\n'
        text += f'x e y sono le coordinate del pixel da piazzare\n'
        text += f'Sovrascrivi una tua casella per cancellarla\n'
        text += str(place)
        show_interaction(update, text)
        # todo AttributeError: 'NoneType' object has no attribute 'reply_text'
        await update.message.reply_text(text)


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /leaderboard is issued."""
    architect = Architect()
    names, emojis, tiles = architect.get_tile_leaderboard()
    text = "---🏆 Leaderboard 🏆 ---\n"
    for i in range(len(names)):
        s = '' if tiles[i] == 1 else 's'
        text += f'{emojis[i]} {names[i]}: {tiles[i]} point{s}\n'
    show_interaction(update, text)
    await update.message.reply_text(text)


# command handlers (without slash, need to be here)
COMMANDS["start"] = start_command
COMMANDS["help"] = help_command
COMMANDS["users"] = get_users_command
COMMANDS["random_user"] = random_user_command
COMMANDS["place"] = place_command
COMMANDS["babbo_natale_segreto"] = babbo_natale_segreto_command
COMMANDS["burp"] = burp_command
COMMANDS["leaderboard"] = leaderboard_command
