"""
Define a few command handlers.
These usually take the two arguments update and context.
"""
from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from time import time, gmtime, strftime
import numpy as np
from src.architect import Architect
from src.place import Place
from scripts.utils import show_interaction
from scripts.utils import get_user_full_name, babbo_natale, get_user_id
from src.admin_commands import ADMIN_COMMNADS, command_wrapper


COMMANDS = dict()
PLACING_TILE_POINTS = 1

CONSOLATION_PHRASES = ["Better luck next time!",
                       "You lost!",
                       "You lose!",
                       "You didn't win!",
                       "You didn't make it!",
                       "You didn't get it!",
                       "You didn't get there!",
                       "Sorry! You didn't win!",
                       "Try again"]


@command_wrapper
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    _ = context.args
    user = update.effective_user
    usern_full_name = get_user_full_name(user)

    Architect().add_user(user.id, usern_full_name)

    text = f"Ciao {user.mention_html()}! " \
           f"Sono Omar2.0, il tuo assistente personale 🤖\n" \
           f"Dimmi cosa posso fare per te! 😺\n" \
           f"Scrivi /help per vedere i comandi disponibili 📚"
    show_interaction(update, text)
    await update.message.reply_html(text, reply_markup=ForceReply(selective=True))


@command_wrapper
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    _ = context.args

    # list of commands
    text = ("🖥 Commands: " + ", ".join(["/" + key for key in COMMANDS]) + "\n")

    # list of admin-only commands
    admin_ids = Architect().get_admin_ids()
    if get_user_id(update) in admin_ids:
        text += "✨ Admin commands: " + ", ".join(["/" + key for key in ADMIN_COMMNADS]) + "\n"

    show_interaction(update, text)
    await update.message.reply_text(text)


@command_wrapper
async def babbo_natale_segreto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /babbo_natale_segreto is issued."""
    architect = Architect()
    _ = context.args
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

        # add user to the list of active santas
        architect.add_active_santa(this_user_id)

        show_interaction(update, text)
        await update.message.reply_text(text)
    else:
        text = 'Non fai parte dei Babbi Natale...'
        show_interaction(update, text)
        await update.message.reply_text(text)


@command_wrapper
async def get_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /users is issued."""
    architect = Architect()
    _ = context.args
    users = [f'{architect.get_user_emoji(i)} {architect.get_user_name(i)}' for i in architect.user_info]
    text = "---👥 Utenti registrati 👥---\n"
    text += '\n'.join(users)
    show_interaction(update, text)
    await update.message.reply_text(text)


@command_wrapper
async def show_user_gems_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /gems is issued."""
    architect = Architect()
    _ = context.args
    user_id = get_user_id(update)
    gems = architect.get_gems(user_id)
    text = f"🔹 You own {gems} gems 🔹"
    show_interaction(update, text)
    await update.message.reply_text(text)


@command_wrapper
async def random_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /random_user is issued."""
    architect = Architect()
    _ = context.args
    user_info = architect.get_user_info()
    random_user_id = list(user_info.keys())[np.random.randint(len(user_info))]
    emoji = architect.get_user_emoji(random_user_id)
    text = f"👥 Utenti registrati: {len(user_info)}\n"
    text += f"👤 Utente casuale: {emoji} {architect.get_user_name(random_user_id)}"
    show_interaction(update, text)
    await update.message.reply_text(text)


@command_wrapper
async def place_command(update: Update, context: ContextTypes.DEFAULT_TYPE, n_gems=1):
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
                architect.increase_gems(user_id, n_gems)
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


@command_wrapper
async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE, length=5):
    """Send a message when the command /leaderboard is issued."""
    architect = Architect()
    _ = context.args
    names, emojis, points = architect.get_tile_leaderboard()
    text = "---🔹 Gems Leaderboard 🔹---\n"
    for i in range(len(names)):
        text += f'{points[i]:_>{length}} {emojis[i]} {names[i]} \n'
    show_interaction(update, text)
    await update.message.reply_text(text)


@command_wrapper
async def play_coin_game(update: Update, context: ContextTypes.DEFAULT_TYPE, n_coins=5, limit=100):
    """Toss n_coins straight heads to win gems."""
    args = context.args
    architect = Architect()
    user_id = get_user_id(update)

    multiplier = round(2 ** n_coins, -1)
    chars = ["🟡", "🔵"]

    if len(args) == 0:
        text = f'🔹 Toss {n_coins} heads {chars[0]} to win {multiplier} times the gems! 🔹\n'
        text += 'Usage: /gamble [n_gems]'
    else:

        # check bet size
        bet = args[0]
        try:
            bet = int(bet)
        except ValueError:
            # invalid bet
            text = f'{bet} is not a valid bet amount\n'
            show_interaction(update, text)
            return await update.message.reply_text(text)

        player_gems = architect.get_gems(get_user_id(update))
        if bet > player_gems:
            text = f'You have only {player_gems} gems 🔹\n'
            show_interaction(update, text)
            return await update.message.reply_text(text)

        if bet > limit:
            text = f'You can bet up to {limit} gems 🔹\n'
            show_interaction(update, text)
            return await update.message.reply_text(text)

        if bet <= 0:
            text = 'You must bet at least 1 gem 🔹\n'
            show_interaction(update, text)
            return await update.message.reply_text(text)

        # if bet went through
        price = bet * multiplier
        text = f'💰 You bet {bet} gems 🔹\n'
        architect.decrease_gems(user_id, bet)

        # toss coins
        coins = np.random.choice([0, 1], n_coins)
        text += f'Coins: {" ".join([chars[i] for i in coins])}\n'
        text += '\n'
        if sum(coins) == 0:
            # reward the player
            text += f'🎉 Congrats! You won {price} gems 🔹 🎉'
            text += f'💰 You now have {player_gems + price} gems 💰'
            architect.increase_gems(user_id, price)
        else:
            if sum(coins) == 1:
                phrase = "Almost there!"
            elif sum(coins) == 0:
                phrase = "Impressive! All tails..."
            else:
                phrase = np.random.choice(CONSOLATION_PHRASES)
            text += f'💸 {phrase} 💸'

    show_interaction(update, text)
    return await update.message.reply_text(text)


def main():
    """List of commands (without slash)"""

    # command handlers
    COMMANDS["start"] = start_command
    COMMANDS["help"] = help_command
    COMMANDS["users"] = get_users_command
    COMMANDS["gems"] = show_user_gems_command
    COMMANDS["random_user"] = random_user_command
    COMMANDS["place"] = place_command
    COMMANDS["babbo_natale_segreto"] = babbo_natale_segreto_command
    COMMANDS["leaderboard"] = leaderboard_command
    COMMANDS["gamble"] = play_coin_game


if __name__ == "src.commands":
    main()
