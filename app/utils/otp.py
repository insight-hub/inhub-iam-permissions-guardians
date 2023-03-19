import random as rand
import string


def get_random_pass(lenght: int = 6):
    return ''.join(rand.choice(string.ascii_lowercase +
                               string.ascii_uppercase +
                               string.digits) for _ in range(lenght))
