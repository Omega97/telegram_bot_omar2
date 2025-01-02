"""
Define a few command handlers.
These usually take the two arguments update and context.
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.architect import Architect
from scripts.pasgen_2024 import generate_password
from scripts.utils import show_interaction
from scripts.utils import get_user_full_name, get_user_id


ADMIN_COMMNADS = dict()


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

    s = "" if len(user_ids) == 1 else "s"
    text = f"👥 {len(user_ids)} user{s}:"
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
async def admin_canvas_names_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get list of canvas names"""
    architect = Architect()
    _ = context.args
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


@check_admin_wrapper
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
        text = "Usage: /set_santa [user_id] [True/False]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_check_santa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check which users already used the santa command this year."""
    architect = Architect()
    _ = context.args

    santas = architect.get_santas()
    active_santas = architect.get_active_santas_ids()

    if len(santas) == 0:
        text = "No santas set!"
    else:
        if len(active_santas) == len(santas):
            text = "All santas used the command this year!"
        else:
            n = len(santas) - len(active_santas)
            text = f"{n} santas didn't use the command yet!"

    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_password_command(update: Update, context: ContextTypes.DEFAULT_TYPE, default_length=16):
    """Generate a password"""
    args = context.args
    text = None

    try:
        key = args[0] if len(args) > 0 else ""
        length = int(args[1]) if len(args) > 1 else default_length
    except ValueError:
        text = 'This command generates a password using a key and a length.\n'
        text += f"Usage: /password [key] [length]"
    else:
        if text is None:
            try:
                username = get_user_full_name(update.effective_user)
                password = generate_password(key, username, length)
                text = f"{password}"
            except ValueError as _:
                text = f"Usage: /password [key] [length]"

    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_give_gems_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Give gems to a user"""
    architect = Architect()
    args = context.args
    if len(args) == 2:
        user_id = int(args[0])
        if user_id not in architect.get_user_ids():
            text = f"User {user_id} not found"
        else:
            gems = int(args[1])

            text = ''
            if gems > 0:
                architect.increase_gems(user_id, gems)
                user_name = architect.get_user_name(user_id)
                s = "" if gems == 1 else "s"
                text += f'🔹 {gems} gem{s} given to user {user_name}\n'
            elif gems < 0:
                architect.decrease_gems(user_id, -gems)
                user_name = architect.get_user_name(user_id)
                s = "" if gems == -1 else "s"
                text += f'🔹 {-gems} gem{s} removed from user {user_name}\n'

            text += f'New total: {architect.get_item(user_id, "gems", 0)} gems 🔹 '
    else:
        text = 'Give gems to a user\n'
        text += "Usage: /give_gems [user_id] [gems]"
    show_interaction(update, text)
    await update.message.reply_text(text)


@check_admin_wrapper
async def admin_list_gems_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all users with their gems, sorted by amount"""
    architect = Architect()
    _ = context.args

    user_ids = architect.get_user_ids()
    gems = {user_id: architect.get_item(user_id, 'gems', 0) for user_id in user_ids}
    sorted_gems = sorted(gems.items(), key=lambda x: x[1], reverse=True)

    text = "🔹 Gems 🔹 \n"
    for user_id, gem in sorted_gems:
        user_name = architect.get_user_name(user_id)
        text += f"{gem:_>5}  {user_name}\n"

    show_interaction(update, text)
    await update.message.reply_text(text)


def main():
    """List of commands (without slash)"""

    # admin command handlers
    ADMIN_COMMNADS["get_ids"] = admin_get_user_ids_command
    ADMIN_COMMNADS["set_emoji"] = admin_set_emoji_command
    ADMIN_COMMNADS["give_gems"] = admin_give_gems_command
    ADMIN_COMMNADS["list_gems"] = admin_list_gems_command
    ADMIN_COMMNADS["canvas_names"] = admin_canvas_names_command
    ADMIN_COMMNADS["set_canvas"] = admin_set_canvas_command
    ADMIN_COMMNADS["get_info"] = admin_get_info_command
    ADMIN_COMMNADS["set_santa"] = admin_set_santa_command
    ADMIN_COMMNADS["check_santa"] = admin_check_santa_command
    ADMIN_COMMNADS["password"] = admin_password_command


if __name__ == "src.admin_commands":
    main()
