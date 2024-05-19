from architect import Architect


architect = Architect()
user_info = architect.get_user_info()

# architect.set_emoji(156267213, '🟦')  # Omar Cusma Fait
# architect.set_emoji(473531951, '🟩')  # Peter Cej
# architect.set_emoji(890008145, '🟨')  # Christopher
# architect.set_emoji(813074514, '🟥')  # Vittorio
# architect.set_emoji(213607266, '🦊')  # Nicolò Rossi

for k in user_info:
    user_info[k]['achievements'] = dict()
    print(k, user_info[k])

architect.save_user_info()
