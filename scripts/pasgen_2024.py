""" Generate password given username and keyword """
from random import randrange, seed, shuffle


ALPHA = ["abcdefghijklmnopqrstuvwxyz",
         "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
         "0123456789",
         "!@#$%^&()+{}|:<>?"]


def gen(length):
    """ Generate string of random char using alphabet """
    types = [i % len(ALPHA) for i in range(length)]
    chars = [ALPHA[i][randrange(len(ALPHA[i]))] for i in types]
    shuffle(chars)
    return ''.join(chars)


def generate_password(key, nickname, length: int, min_length=8, max_length=100):
    """ Generate password given nickname and key """
    if len(key) == 0:
        raise ValueError('Key is empty')
    if nickname == 0:
        raise ValueError('Nickname is empty')
    if length < min_length:
        raise ValueError(f'Length is less than {min_length}')
    if length > max_length:
        raise ValueError(f'Length is more that {max_length}')
    s = nickname + key
    s = s.replace(' ', '')
    s = s.lower()
    seed(s)
    return gen(length=length)
