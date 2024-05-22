import pickle
from architect import Architect


def test_architecture():
    architect = Architect()
    user_info = architect.get_user_info()

    # architect.set_emoji(156267213, '🟦')  # Omar Cusma Fait '🇸🇮'
    # architect.set_emoji(473531951, '🟩')  # Peter Cej
    # architect.set_emoji(890008145, '🇮🇹')  # Christopher 🇮🇹🟨
    # architect.set_emoji(813074514, '🟥')  # Vittorio
    # architect.set_emoji(213607266, '🦊')  # Nicolò Rossi
    # architect.set_emoji(197127934, '🐧')  # Kleit Rrokja
    # architect.set_emoji(130266190, '🦧')  # Simone Mezzavilla 🟪
    # architect.set_emoji(231576312, '😺')  # Eleonora Zanetti
    # architect.set_emoji(6445560359, '🔥')  # Uros
    # architect.set_emoji(6337524767, '🦊')  # Luis
    # architect.set_emoji(734566340, '🚀')  # Edo
    # architect.set_emoji(1474749149, '🦙')  # Tanja

    # change user canvas
    architect.set_item(156267213, 'canvas', 'default')  # default, friends

    # print(user_info)
    for user_id in user_info:
        # print user info
        print(f'\nid: {user_id}')
        for k, v in user_info[user_id].items():
            print(f'{k}: {v}')

    # print the number of users
    print(f'\n{len(user_info)} users registered')

    # save the user info
    architect.save_user_info()


def test_place():
    path = 'data/place.pkl'
    with open(path, 'rb') as f:
        grid = pickle.load(f)
    with open(path, 'wb') as f:
        pickle.dump(grid, f)


if __name__ == '__main__':
    test_architecture()
    # test_place()
