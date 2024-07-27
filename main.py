"""
Telegram bot
telegram version 21.1.1

Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic bot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

# todo check string conversion to int
# todo check for canvas name il existing canvases
# todo save ALL messages
# todo blocked users
# todo canvas of given size
# todo class for handlers?
# todo admin set admin?
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.my_handlers import *
from src.my_reply import reply
from src.my_handlers import COMMANDS, ADMIN_COMMNADS
from scripts.utils import read_file


# Read the token from the file
token_path = 'data\\TOKEN.txt'
TOKEN = read_file(token_path)


# Enable logging and set higher logging level for httpx
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    for command in COMMANDS:
        application.add_handler(CommandHandler(command, COMMANDS[command]))
    for command in ADMIN_COMMNADS:
        application.add_handler(CommandHandler(command, ADMIN_COMMNADS[command]))

    # on non command i.e. text message - reply to the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
