import random
import requests
import allure
import json
from user import User
from faker import Faker

faker = Faker()

class TestTakeOrder:
    @allure.title('Проверка получения ответа об успешном принятии заказа')
    def test_take_order(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        payload = {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "address": faker.street_address(),
            "metroStation": random.randint(0, 333),
            "phone": faker.phone_number(),
            "rentTime": random.randint(0, 7),
            "deliveryDate": f"2024-02-{random.randint(1, 29)}",
            "comment": "Please leave at the gates",
            "color": [
                "BLACK"
            ]
        }
        payload_string = json.dumps(payload)
        response = requests.post(f"{url}/api/v1/orders", data=payload_string)
        id_order = response.json()["track"]
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response_post = requests.post(f"{url}/api/v1/courier/login", data=payload)
        id_courier = response_post.json()['id']
        response_put = requests.put(f"{url}/api/v1/orders/accept/{id_order}?courierId={id_courier}")
        assert '{"ok":true}' in response_put.text

    @allure.title('Попытка принять заказ без указания id курьера')
    def test_take_order_without_id_courier(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        payload = {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "address": faker.street_address(),
            "metroStation": random.randint(0, 333),
            "phone": faker.phone_number(),
            "rentTime": random.randint(0, 7),
            "deliveryDate": f"2024-02-{random.randint(1, 29)}",
            "comment": "Please leave at the gates",
            "color": [
                "BLACK"
            ]
        }
        payload_string = json.dumps(payload)
        response_post = requests.post(f"{url}/api/v1/orders", data=payload_string)
        id_order = response_post.json()["track"]
        response_put = requests.put(f"{url}/api/v1/orders/accept/{id_order}?courierId=")
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_put.text and 400 == response_put.status_code

    @allure.title('Попытка принять заказ с указанием неверного id курьера')
    def test_take_order_with_incorrect_id_courier(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        payload = {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "address": faker.street_address(),
            "metroStation": random.randint(0, 333),
            "phone": faker.phone_number(),
            "rentTime": random.randint(0, 7),
            "deliveryDate": f"2024-02-{random.randint(1, 29)}",
            "comment": "Please leave at the gates",
            "color": [
                "BLACK"
            ]
        }
        payload_string = json.dumps(payload)
        response_post = requests.post(f"{url}/api/v1/orders", data=payload_string)
        id_order = response_post.json()["track"]
        id_courier = random.randint(1000000, 9999999)
        response_put = requests.put(f"{url}/api/v1/orders/accept/{id_order}?courierId={id_courier}")
        error_message = "Курьера с таким id не существует"
        assert error_message in response_put.text and 404 == response_put.status_code

    @allure.title('Попытка принять заказ без указания id заказа')
    def test_take_order_without_id_order(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response_post = requests.post(f"{url}/api/v1/courier/login", data=payload)
        id_courier = response_post.json()['id']
        response_put = requests.put(f"{url}/api/v1/orders/accept/courierId={id_courier}")
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_put.text and 400 == response_put.status_code

    @allure.title('Попытка принять заказ с указанием неверного id заказа')
    def test_take_order_with_incorrect_id_order(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response_post = requests.post(f"{url}/api/v1/courier/login", data=payload)
        id_courier = response_post.json()['id']
        id_order = random.randint(1000000, 9999999)
        response_put = requests.put(f"{url}/api/v1/orders/accept/{id_order}?courierId={id_courier}")
        error_message = "Заказа с таким id не существует"
        assert error_message in response_put.text and 404 == response_put.status_code








