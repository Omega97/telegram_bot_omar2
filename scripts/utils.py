from telegram import Update
import numpy as np
from time import time, gmtime, strftime
import os


DEFAULT_EMOJI = ["⬜️", "🟥", "🟧", "🟨", "🟩", "🟪",
                 "⚪", "🟠", "🟡", "🟢", "🔵", "🟣",
                 "🐶", "🐱", "🦊", "🐭", "🐹", "🐰",
                 "🐻", "🐼", "🐯", "🦁", "🐬", "🐧",
                 "🦖", "🍀", "⚡️", "🔥", "⭐️", "☀️",
                 "🍎", "🍓", "🍒", "🍉", "🍕", "🍣",
                 "⚽️", "🏀", "🥎", "💎", "💻", "🚀",
                 "🍪", "🛑", "❇️"]


def read_file(file_name, encoding='utf-8'):
    """Read the token from the file"""
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Please create the {file_name} file")
    with open(file_name, "r", encoding=encoding) as f:
        token = f.read().strip()
    return token


def get_user_full_name(user):
    """Return the full name of the user who sent the message"""
    return f"{user.first_name} {user.last_name}" if user.last_name else user.first_name


def get_message_text(update):
    """Return the text of the message"""
    out = 'None'
    if hasattr(update.message, 'text'):
        out = str(update.message.text)
    return out


def get_user_id(update):
    """Return the id of the user who sent the message"""
    return update.effective_user.id


def show_interaction(update: Update, reply_text: str):
    username = get_user_full_name(update.effective_user)
    user_message = get_message_text(update)
    t_string = strftime("%H:%M:%S", gmtime(time()))
    print(f"\n[{t_string}] {username}: {user_message}")
    print(f">>> {reply_text}")


def pick_random_gift_receivers(n, seed):
    """Pick random gift receivers for the Babbo Natale Segreto game"""
    np.random.seed(seed)
    v = list(np.random.permutation(n))
    return [v[v.index(i) - 1] for i in range(n)]


def babbo_natale(names: list) -> dict:
    """Return the secret Santa for each user in the list of names"""
    names = np.array(names)
    year = strftime("%Y", gmtime())
    indices = pick_random_gift_receivers(len(names), int(year))
    receivers = {names[i]: names[j] for i, j in enumerate(indices)}
    return receivers


def generic_convert_string(s: str):
    """ try to convert the value to int, float, or bool  todo check! """

    # string
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]

    # empty string
    if s == '':
        return None

    # None
    if s == 'None':
        return None

    # int
    try:
        return int(s)
    except ValueError:
        pass

    # float
    try:
        return float(s)
    except ValueError:
        pass

    # bool
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False

    return s


def read_user_csv_file(file_name):
    """Convert the csv user file to a dictionary"""
    out = dict()
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            v = line.strip().split(",")
            key = v[0]
            value = ','.join(v[1:])
            out[key] = generic_convert_string(value)
    return out


def write_user_csv_file(file_name, user_info):
    """Write the user dictionary to a csv file"""
    s = ''
    for key in user_info:
        value = user_info[key]
        s += f'{key},{value}\n'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(s)


def moderate(text, word_path='data/bad_words.txt'):
    """Return the text without bad words"""
    with open(word_path, 'r') as f:
        bad_words = f.read().splitlines()
    for bad_word in bad_words:
        if len(bad_word) < 5:
            continue
        text = text.replace(bad_word, '*' * len(bad_word))
    return text
