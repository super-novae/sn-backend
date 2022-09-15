import random
import string


def generate_password():
    letters = "".join(random.sample(string.ascii_letters, 6))
    digits = "".join(random.sample(string.digits, 2))
    special_chars = "".join(random.sample("#$@&*?", 2))
    password = letters + digits + special_chars
    return password
