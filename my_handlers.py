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
from place import Place
from misc import get_user_full_name, babbo_natale, get_user_id
from pasgen_2024 import generate_password


COMMANDS = dict()
ADMIN_COMMNADS = dict()
PLACING_TILE_POINTS = 1


async def start_command(update: Update, _):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    usern_full_name = get_user_full_name(user)

    Architect().add_user(user.id, usern_full_name)

    text = f"Ciao {user.mention_html()}! " \
           f"Sono Omar2.0, il tuo assistente personale 🤖\n" \
           f"Dimmi cosa posso fare per te! 😺\n" \
           f"Scrivi /help per vedere i comandi disponibili 📚"
    show_interaction(update, text)
    await update.message.reply_html(text, reply_markup=ForceReply(selective=True))


async def help_command(update: Update, _):
    """Send a message when the command /help is issued."""
    # list of commands
    text = ("🖥 Commands: " + ", ".join(["/" + key for key in COMMANDS]) + "\n")

    # list of admin-only commands
    admin_ids = Architect().get_admin_ids()
    if get_user_id(update) in admin_ids:
        text += "✨ Admin commands: " + ", ".join(["/" + key for key in ADMIN_COMMNADS]) + "\n"

    show_interaction(update, text)
    await update.message.reply_text(text)


async def babbo_natale_segreto_command(update: Update, _):
    """Send a message when the command /babbo_natale_segreto is issued."""
    architect = Architect()
    santas = architect.get_santas()
    user_names = [architect.get_user_name(user_id) for user_id in santas]
    this_user = get_user_full_name(update.effective_user)
    this_user_id = get_user_id(update)

    if this_user_id in santas:
        text = "🎄☃❄ Babbo Natale Segreto! 🎅🎁🎄\n\n"
        text += f"👥 Utenti registrati: {len(user_names)} (Assicurati che ci siate tutti!!!)\n"
        for name in user_names:
            text += f'- {name}\n'
        text += '\n'
        year = strftime("%Y", gmtime())
        text += f'Il tuo Babbo Natale segreto {year} è:\n➡{babbo_natale(user_names)[this_user]}⬅ !'
        show_interaction(update, text)
        await update.message.reply_text(text)
    else:
        text = 'Non fai parte dei Babbi Natale...'
        show_interaction(update, text)
        await update.message.reply_text(text)


async def get_users_command(update: Update, _):
    """Send a message when the command /users is issued."""
    architect = Architect()
    users = [f'{architect.get_user_emoji(i)} {architect.get_user_name(i)}' for i in architect.user_info]
    text = "---👥 Utenti registrati 👥---\n"
    text += '\n'.join(users)
    show_interaction(update, text)
    await update.message.reply_text(text)


async def burp_command(update: Update, _):
    """Send a message when the command /burp is issued."""
    text = "Ma Omar!"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def random_user_command(update: Update, _):
    """Send a message when the command /random_user is issued."""
    architect = Architect()
    user_info = architect.get_user_info()
    random_user_id = list(user_info.keys())[np.random.randint(len(user_info))]
    emoji = architect.get_user_emoji(random_user_id)
    text = f"👥 Utenti registrati: {len(user_info)}\n"
    text += f"👤 Utente casuale: {emoji} {architect.get_user_name(random_user_id)}"
    show_interaction(update, text)
    await update.message.reply_text(text)


async def place_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /place is issued."""
    architect = Architect()
    user_id = update.effective_user.id
    canvas_name = architect.get_canvas_name(user_id)
    place = Place(canvas_name=canvas_name)
    args = context.args
    text = ''
    now = time()

    if len(args) >= 2:
        # coordinates
        last_place_time = architect.get_last_place_time(user_id)
        time_to_wait = 0

        if last_place_time is not None:
            time_to_wait = place.minutes_cooldown * 60 - now + last_place_time

        if time_to_wait <= 0:
            # place the pixel
            x = None
            y = None
            user_id = None
            try:
                x = int(args[0])
                y = int(args[1])
                user_id = update.effective_user.id
                place.swap_pixel(x, y, user_id=user_id)
                architect.set_last_place_time(user_id, now)
                architect.add_place_tiles_count(user_id)
                architect.increase_points(user_id, PLACING_TILE_POINTS)
                text += str(place)
            except Exception as e:
                text = (f"{x} {y} {user_id}\n"
                        f"{e}: I valori inseriti non sono validi!")

            show_interaction(update, text)
            await update.message.reply_text(text)
        else:
            # wait
            text += f'💤 mancano ancora {time_to_wait+1:.0f} secondi...\n'
            show_interaction(update, text)
            if update.message is not None:
                await update.message.reply_text(text)
            else:
                await update.callback_query.answer(text)  # todo check
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
        elif args[0] == 'tiles':
            count = place.count_tiles()
            count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}
            ids = list(count.keys())
            emojis = [architect.get_user_emoji(i) for i in ids]
            names = [architect.get_user_name(i) for i in ids]
            text = f"---🏆 Tiles on the Canvas 🏆 ---\n"
            for i in range(len(ids)):
                text += f'{count[ids[i]]} {emojis[i]} {names[i]}\n'
            show_interaction(update, text)
            await update.message.reply_text(text)
    else:
        # show canvas
        text += f'Piazza un emoji ogni {place.minutes_cooldown} minuti con /place [x] [y]\n'
        text += f'Sovrascrivi una tua casella per cancellarla\n'
        text += f'/place stats, /place tiles per vedere le statistiche\n'
        text += str(place)
        show_interaction(update, text)
        # todo AttributeError: 'NoneType' object has no attribute 'reply_text'
        await update.message.reply_text(text)


async def leaderboard_command(update: Update, _):
    """Send a message when the command /leaderboard is issued."""
    architect = Architect()
    names, emojis, points = architect.get_tile_leaderboard()
    text = "---🏆 Leaderboard 🏆---\n"
    text += 'Punti di ciascun utente:\n'
    for i in range(len(names)):
        text += f'{points[i]} {emojis[i]} {names[i]} \n'
    show_interaction(update, text)
    await update.message.reply_text(text)


def check_admin_wrapper(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = get_user_id(update)
        architect = Architect()
        if architect.is_admin(user_id):
            await func(update, context)
        else:
            text = "Non sei un admin!"
            show_interaction(update, text)
            await update.message.reply_text(text)

    return wrapper


@check_admin_wrapper
async def admin_get_user_ids_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get list of ids and usernames """
    args = context.args
    architect = Architect()

    if len(args) == 0:
        user_ids = architect.get_user_ids()
    else:
        user_ids = architect.smart_id_search(args[0])

    text = f"👥 {len(user_ids)} users:"
    for user_id in sorted(user_ids):
        text += f"\n{user_id} {architect.get_user_name(user_id)}"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_set_emoji_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set user's emoji"""
    architect = Architect()
    args = context.args
    if len(args) == 2:
        user_id = int(args[0])
        if user_id not in architect.get_user_ids():
            text = f"User {user_id} not found"
        else:
            emoji = args[1]
            architect.set_user_emoji(user_id, emoji)
            text = f"Set emoji {emoji} for user {user_id}"
    else:
        text = "Usage: /set_emoji [user_id] [emoji]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_canvas_names_command(update: Update, _):
    """Get list of canvas names"""
    architect = Architect()
    canvas_names = architect.get_canvas_names()
    text = f"🎨 {len(canvas_names)} canvases:"
    for canvas_name in canvas_names:
        text += f"\n- {canvas_name}"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_set_canvas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set user's canvas"""
    architect = Architect()
    args = context.args
    if len(args) == 2:
        user_id = int(args[0])
        if user_id not in architect.get_user_ids():
            text = f"User {user_id} not found"
        else:
            canvas = f'{args[1].lower()}.csv'

            if canvas in architect.get_canvas_names():
                architect.set_canvas(user_id, canvas)
                text = f'🎨 Canvas "{canvas}" set for user {user_id}'
            else:
                text = f'Canvas "{canvas}" not found!'
    else:
        text = "Usage: /set_canvas [user_id] [canvas]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@ check_admin_wrapper
async def admin_get_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's info"""
    architect = Architect()
    args = context.args
    if len(args) == 1:
        user_id = int(args[0])
        if user_id not in architect.get_user_ids():
            text = f"User {user_id} not found"
        else:
            text = f"Info for user {user_id}:\n"
            text += f"Name: {architect.get_user_name(user_id)}\n"
            text += f"Emoji: {architect.get_user_emoji(user_id)}\n"
            text += f"Canvas: {architect.get_canvas_name(user_id)}\n"
            text += f"Admin: {architect.get_item(user_id, 'admin', False)}"
    else:
        text = "Usage: /get_info [user_id]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_set_santa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set user's santa"""
    architect = Architect()
    args = context.args
    if len(args) == 2:
        user_id = int(args[0])
        if user_id not in architect.get_user_ids():
            text = f"User {user_id} not found"
        else:
            santa = args[1].lower().startswith('t')
            architect.set_santa(user_id, santa)
            text = f'🎅 Santa set to "{santa}" for user {user_id}'
    else:
        text = "Usage: /set_santa [user_id] [santa]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_password_command(update: Update, context: ContextTypes.DEFAULT_TYPE, default_length=16):
    """Generate a password"""
    args = context.args
    key = ""
    length = default_length
    text = None

    try:
        key = args[0] if len(args) > 0 else ""
        length = int(args[1]) if len(args) > 1 else default_length
    except Exception:
        text = f"Usage: /password [key] [length]"
    else:
        if text is None:
            try:
                username = get_user_full_name(update.effective_user)
                password = generate_password(key, username, length)
                text = f"{password}"
            except Exception as _:
                text = f"Usage: /password [key] [length]"

    show_interaction(update, text)
    await update.message.reply_text(text)


# command handlers (without slash, need to be here)
COMMANDS["start"] = start_command
COMMANDS["help"] = help_command
COMMANDS["users"] = get_users_command
COMMANDS["random_user"] = random_user_command
COMMANDS["place"] = place_command
COMMANDS["babbo_natale_segreto"] = babbo_natale_segreto_command
COMMANDS["leaderboard"] = leaderboard_command

# admin commands
ADMIN_COMMNADS["get_ids"] = admin_get_user_ids_command
ADMIN_COMMNADS["set_emoji"] = admin_set_emoji_command
ADMIN_COMMNADS["canvas_names"] = admin_canvas_names_command
ADMIN_COMMNADS["set_canvas"] = admin_set_canvas_command
ADMIN_COMMNADS["get_info"] = admin_get_info_command
ADMIN_COMMNADS["set_santa"] = admin_set_santa_command
ADMIN_COMMNADS["password"] = admin_password_command
