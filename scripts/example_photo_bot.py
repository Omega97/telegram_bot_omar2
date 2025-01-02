"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot.py to see the same
example built on the telegram.ext bot framework.
"""
import logging
import asyncio
import contextlib
import os
from typing import NoReturn
from telegram import Bot, Update
from telegram.error import Forbidden, NetworkError
from scripts.utils import read_file


# Read the token from the file
token_path = 'data\\TOKEN.txt'
TOKEN = read_file(token_path)

# logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def photo_handler(bot: Bot, update: Update, dir_path='data\\photos') -> None:
    """Download the photo sent by the user"""
    photo_file = update.message.photo[-1]  # Get the last photo in the list of photos
    file_id = photo_file.file_id
    file_obj = await bot.get_file(file_id)

    # Construct the filename (adjust as needed)
    os.makedirs(dir_path, exist_ok=True)
    filename = os.path.join(dir_path, f"{update.message.message_id}.jpg")

    # Download the photo to the current directory
    await file_obj.download_to_drive(custom_path=filename)

    logger.info(f"Downloaded photo: {filename}")
    await update.message.reply_text("Photo downloaded successfully!")


async def echo(bot: Bot, update_id: int) -> int:
    """Echo the message the user sent"""
    # The bot request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10, allowed_updates=Update.ALL_TYPES)
    for update in updates:
        next_update_id = update.update_id + 1

        if update.message:

            if update.message.text:
                # Echo text messages
                logger.info("Found message %s!", update.message.text)
                await update.message.reply_text(update.message.text)
            elif update.message.photo:
                # Download and handle photos
                await photo_handler(bot, update)

        return next_update_id
    return update_id


async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with Bot(TOKEN) as bot:
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.
        try:
            update_id = (await bot.get_updates())[0].update_id
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        while True:
            try:
                update_id = await echo(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):  # to ignore exception when Ctrl-C is pressed
        asyncio.run(main())
