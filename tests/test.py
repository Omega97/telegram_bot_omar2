from src.architect import Architect
from src.place import Place
from scripts.utils import read_file
import numpy as np


def test_show_user_info():
    architect = Architect(data_dir="..\\DATA")
    user_info = architect.get_user_info()

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


def test_mini_canvas():
    place = Place('maxi', shape=(16, 40))
    print(place)


def test_characters(file_path='..\\DATA\\default_emoji.txt'):
    s = read_file(file_path)
    v = [c for c in s]
    for c in v:
        print(c, ord(c))


def test_photo():
    architect = Architect(data_dir="..\\DATA")
    names = architect.get_photo_names()
    print(names)
    img = architect.get_photo(names[0])
    # cv2.imshow(names[0], img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    v = np.mean(np.mean(img, axis=0), axis=0)
    v = np.round(v)
    print(v)


def test_architect():
    architect = Architect(data_dir="..\\DATA")
    for user_id in architect.get_user_info():
        print()
        print(user_id)
        for key, value in architect.user_info[user_id].items():
            print(f'{key}: {value} \033[90m{type(value)}\033[0m')
    architect.save_user_info()


def test_architect_2():
    """Modify user data"""
    architect = Architect(data_dir="..\\DATA")
    database = architect.get_user_info()
    for user_id in database:
        user_info = database[user_id]
        print()
        print(user_id)
        print(user_info[user_id])
    architect.save_user_info()


if __name__ == '__main__':
    # test_show_user_info()
    # test_mini_canvas()
    # test_characters()
    # test_photo()
    # test_architect()
    test_architect_2()
