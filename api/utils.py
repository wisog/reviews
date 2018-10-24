from random import choice
from string import ascii_uppercase

from . import models

import datetime

MESSAGES = {
    'NO_KEY': 'should provide a valid authkey param',
    'BAD_KEY': 'invalid authkey',
    'REVIEW_NOT_FOUND': "review doesn't exist or deleted",
    'BAD_METHOD': 'method not supported'
}

def generate_auth_key():
    return ''.join(choice(ascii_uppercase) for i in range(20))


def get_user_from_key(key):
    try:
        user = models.User.objects.get(auth_key=key)
        return user
    except models.User.DoesNotExist:
        return None

def generate_review_from_data(data):
 pass
def get_today_as_string():
    return str(datetime.date.today())