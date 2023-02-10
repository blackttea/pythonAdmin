import random


def gen_verify_code(length=4):
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choices(all_chars, k=length))