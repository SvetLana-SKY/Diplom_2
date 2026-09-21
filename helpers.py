import random
import string
import requests
from urls import Urls


def generate_email():
    name = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"{name}@yandex.ru"


def generate_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_name():
    return "User_" + "".join(random.choices(string.ascii_lowercase, k=6))

def get_ingredients_hash():
    """Получить список ингредиентов с сервера."""
    response = requests.get(Urls.GET_INGREDIENTS)
    data = response.json()["data"]
    return [item["_id"] for item in data]