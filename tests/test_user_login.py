import allure
import requests

from urls import Urls
from helpers import generate_email, generate_password
from data import Messages


class TestLogin:

    @allure.title("Вход под существующим пользователем")
    @allure.description("Проверка: код 200, success=true, есть токены, email и name совпадают")
    def test_login_existing_user(self, registered_user):
        with allure.step("Получение данных зарегистрированного пользователя"):
            payload = {
                "email": registered_user["payload"]["email"],
                "password": registered_user["payload"]["password"],
            }

        with allure.step("Отправка POST-запроса на авторизацию"):
            response = requests.post(
                Urls.LOGIN_USER,
                json=payload)

        
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body
            assert body["user"]["email"] == payload["email"]
            assert body["user"]["name"] == registered_user["payload"]["name"]



    @allure.title("Вход с неверным логином и паролем")
    @allure.description("Проверка: код 401, success=false, message=email or password are incorrect")
    def test_login_incorrect_data(self):
        with allure.step("Генерация несуществующих данных"):
            payload = {
                "email": generate_email(),
                "password": generate_password(),
            }

        with allure.step("Отправка POST-запроса на авторизацию"):
            response = requests.post(
                Urls.LOGIN_USER,
                json=payload)
                

       
            assert response.status_code == 401       
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.INCORRECT_DATA