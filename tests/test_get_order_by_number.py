import random
import allure
import requests
import json
from faker import Faker

faker = Faker()

class TestTakeOrder:
    @allure.title('Проверка получения заказа при успешном запросе')
    def test_get_order_by_number(self):
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
        response_get = requests.get(f"{url}/api/v1/orders/track?t={id_order}")
        assert "order" in response_get.text and 200 == response_get.status_code

    @allure.title('Попытка получить заказ без номера')
    def test_get_order_without_number(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        response_get = requests.get(f"{url}/api/v1/orders/track?t=")
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_get.text

    @allure.title('Попытка получить заказ по несуществующему номеру')
    def test_get_order_with_non_existent_number(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        id_order = random.randint(1000000, 9999999)
        response_get = requests.get(f"{url}/api/v1/orders/track?t={id_order}")
        error_message = "Заказ не найден"
        assert error_message in response_get.text


