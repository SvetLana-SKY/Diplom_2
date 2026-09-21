import pytest
import allure
import requests

from urls import Urls
from helpers import generate_email, generate_password, generate_name
from data import Messages


class TestUserRegistration:


    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка: код 200, success=true, есть токены, email и name совпадают")
    def test_create_unique_user(self, delete_user_after_test):
        with allure.step("Генерация данных пользователя"):
            payload = {
                "email": generate_email(),
                "password": generate_password(),
                "name": generate_name(),
            }

        with allure.step("Отправка POST-запроса на регистрацию"):
            response = requests.post(
                Urls.REGISTER_USER,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Проверка статус-кода 200"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body
            assert body["user"]["email"] == payload["email"]
            assert body["user"]["name"] == payload["name"]

        with allure.step("Регистрация токена для удаления"):
            delete_user_after_test(body["accessToken"])


    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Проверка: код 403, message=User already exists")
    def test_create_duplicate_user(self, registered_user):
        with allure.step("Получение данных уже зарегистрированного пользователя"):
            payload = registered_user["payload"]

        with allure.step("Отправка POST-запроса с теми же данными"):
            response = requests.post(
                Urls.REGISTER_USER,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Проверка статус-кода 403"):
            assert response.status_code == 403

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.EXISTS_USER


    @allure.title("Создание пользователя без поля email")
    @allure.description("Проверка: код 403, message=Email, password and name are required fields")
    def test_create_user_without_email(self):
        with allure.step("Генерация данных без email"):
            payload = {"password": generate_password(), "name": generate_name()}

        with allure.step("Отправка POST-запроса"):
            response = requests.post(
                Urls.REGISTER_USER,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Проверка статус-кода 403"):
            assert response.status_code == 403

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.REQUIRED_FIELDS


    @allure.title("Создание пользователя без поля password")
    @allure.description("Проверка: код 403, message=Email, password and name are required fields")
    def test_create_user_without_password(self):
        with allure.step("Генерация данных без password"):
            payload = {"email": generate_email(), "name": generate_name()}

        with allure.step("Отправка POST-запроса"):
            response = requests.post(
                Urls.REGISTER_USER,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Проверка статус-кода 403"):
            assert response.status_code == 403

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.REQUIRED_FIELDS


    @allure.title("Создание пользователя без поля name")
    @allure.description("Проверка: код 403, message=Email, password and name are required fields")
    def test_create_user_without_name(self):
        with allure.step("Генерация данных без name"):
            payload = {"email": generate_email(), "password": generate_password()}

        with allure.step("Отправка POST-запроса"):
            response = requests.post(
                Urls.REGISTER_USER,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Проверка статус-кода 403"):
            assert response.status_code == 403

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.REQUIRED_FIELDS