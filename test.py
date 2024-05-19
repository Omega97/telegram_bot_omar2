from architect import Architect


architect = Architect()
user_info = architect.get_user_info()

ids = [156267213, 473531951, 890008145, 813074514, 213607266, 197127934, 130266190]

# architect.set_emoji(156267213, '🇸🇮')  # Omar Cusma Fait
# architect.set_emoji(473531951, '🟩')  # Peter Cej
# architect.set_emoji(890008145, '🇮🇹')  # Christopher 🇮🇹🟨
# architect.set_emoji(813074514, '🟥')  # Vittorio
# architect.set_emoji(213607266, '🦊')  # Nicolò Rossi
# architect.set_emoji(197127934, '🐧')  # Kleit Rrokja
# architect.set_emoji(130266190, '🦧')  # Simone Mezzavilla 🟪

# print(user_info)

# for user_id in ids:
#   architect.set_santa(user_id)

for user_id in user_info:
    print(f'\nid: {user_id}')
    for k, v in user_info[user_id].items():
        print(f'{k}: {v}')

print(f'\n{len(user_info)} users registered')

architect.save_user_info()
