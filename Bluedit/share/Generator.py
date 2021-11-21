import uuid
import random
import string
import datetime
import pyotp


class Generator(object):
    # Generate an unique id using user's mac + current timestamp
    # Extremely low chance of collision
    def generate_id(self):
        return str(uuid.uuid1()).replace("-", "")

    # Generate current time
    def generate_time(self):
        f = '%Y-%m-%d %H:%M:%S'
        return datetime.datetime.now().strftime(f)