import allure
import requests

from urls import Urls
from helpers import get_ingredients_hash
from data import Messages, Hash


class Test_Create_Order:


    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Проверка: код 200, success=true, есть номер заказа")
    def test_create_order_with_auth_and_ingredients(self, registered_user):
        with allure.step("Получение токена и ингредиентов"):
            token = registered_user["response"].json()["accessToken"]
            ingredients = get_ingredients_hash()[:2]

        with allure.step("Отправка POST-запроса с авторизацией и ингредиентами"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": ingredients},
                headers={
                    "Authorization": token,
                },
            )

        
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "order" in body
            assert "number" in body["order"] and body["order"]["number"] > 0


    @allure.title("Создание заказа с авторизацией без ингредиентов")
    @allure.description("Проверка: код 400, success=false, message об обязательных ингредиентах")
    def test_create_order_with_auth_without_ingredients(self, registered_user):
        with allure.step("Получение токена"):
            token = registered_user["response"].json()["accessToken"]

        with allure.step("Отправка POST-запроса с пустым списком ингредиентов"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": []},
                headers={
                    "Authorization": token,
                },
            )

        
            assert response.status_code == 400
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.INGREDIENT_REQUIRED




    @allure.title("Создание заказа с авторизацией и неверным хешем ингредиентов")
    @allure.description("Проверка: заказ не создан, success=false")
    def test_create_order_with_auth_invalid_hash(self, registered_user):
        with allure.step("Получение токена"):
            token = registered_user["response"].json()["accessToken"]

        with allure.step("Отправка POST-запроса с неверным хешем"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": Hash.INCORRECT_HASH},
                headers={
                    "Authorization": token,
                },
            )

            assert response.status_code == 500
               


    @allure.title("Создание заказа без авторизации с ингредиентами")
    @allure.description("Проверка: код 200, success=true, есть номер заказа")
    def test_create_order_without_auth_and_ingredients(self):
        with allure.step("Получение ингредиентов"):
            ingredients = get_ingredients_hash()[:2]

        with allure.step("Отправка POST-запроса с ингредиентами"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": ingredients},
                 )

        
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "order" in body
            assert "number" in body["order"] and body["order"]["number"] > 0


    @allure.title("Создание заказа без авторизации без ингредиентов")
    @allure.description("Проверка: код 400, success=false, message об обязательных ингредиентах")
    def test_create_order_without_auth_without_ingredients(self):
        
        with allure.step("Отправка POST-запроса с пустым списком ингредиентов"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": []},
               
            )

        
            assert response.status_code == 400
            body = response.json()
            assert body["success"] is False
            assert body["message"] == Messages.INGREDIENT_REQUIRED




    @allure.title("Создание заказа без авторизации и с неверным хешем ингредиентов")
    @allure.description("Проверка: заказ не создан, success=false")
    def test_create_order_without_auth_invalid_hash(self):
     
        with allure.step("Отправка POST-запроса с неверным хешем"):
            response = requests.post(
                Urls.CREATE_ORDER,
                json={"ingredients": Hash.INCORRECT_HASH},
            )

            assert response.status_code == 500

               
                