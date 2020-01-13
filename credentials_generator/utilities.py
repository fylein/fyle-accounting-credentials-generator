import base64
import random


def string_to_base64(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode()


# Returns a securely generated random string. Source from the django.utils.crypto module.
def get_random_string(length, allowed_chars='abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))


# Create a random secret key. Source from the django.utils.crypto module.
def get_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return get_random_string(40, chars)
