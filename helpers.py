import random
import string


def generate_email():
    name = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"{name}@yandex.ru"


def generate_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_name():
    return "User_" + "".join(random.choices(string.ascii_lowercase, k=6))

