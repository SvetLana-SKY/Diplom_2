
import pytest
import requests

from urls import Urls
from helpers import generate_email, generate_password, generate_name


@pytest.fixture
def registered_user():
    """Создаёт пользователя, возвращает данные, удаляет после теста."""
    payload = {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_name(),
    }
    response = requests.post(
        Urls.REGISTER_USER,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    user_data = response.json()
    access_token = user_data.get("accessToken")

    yield {
        "payload": payload,
        "response": response,
        "user_data": user_data,
        "access_token": access_token,
    }

    if access_token:
        requests.delete(
            Urls.DELETE_USER,
            headers={"Authorization": access_token},
        )

@pytest.fixture
def delete_user_after_test():
    """Собирает токены и удаляет пользователей после теста."""
    tokens = []

    def add_token(token):
        tokens.append(token)

    yield add_token

    for token in tokens:
        requests.delete(Urls.DELETE_USER, headers={"Authorization": token})


