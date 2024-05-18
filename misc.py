import numpy as np
from time import gmtime, strftime
from telegram import Update


def get_user_full_name(user):
    return f"{user.first_name} {user.last_name}" if user.last_name else user.first_name


def show_interaction(update: Update, reply_text: str):
    username = get_user_full_name(update.effective_user)
    user_message = update.message.text
    print(f"\n{username}: {user_message}")
    print(f">>> {reply_text}")


def pick_random_gift_receivers(n, seed):
    np.random.seed(seed)
    v = list(np.random.permutation(n))
    return [v[v.index(i) - 1] for i in range(n)]


def babbo_natale(names: list) -> dict:
    names = np.array(names)
    year = strftime("%Y", gmtime())
    indices = pick_random_gift_receivers(len(names), int(year))
    receivers = {names[i]: names[j] for i, j in enumerate(indices)}
    return receivers


def random_catch_phrase(user, text):
    phrases = [
        text,
        text + "?",
        f"Ciao {user}",
        f"__{user} è esplos@\nper favorire la digestione__",
        "Sto giocando da solo!",
        "Se ci pensi è ovvio",
        "Buondì",
        "Oof",
        "Eh, sì, beh, certo...",
        "Che meme",
        "Sono un bot, non posso fare tutto!",
        "Say to him YOU DOESN'T!",
        "🤖?",
        "🦊?",
        "🦊??",
        "🦊???",
        "Why are you in the isn't of the doesn't?",
        "We don't do that here...",
        "Buongiorno a lei",
    ]
    return np.random.choice(phrases)
