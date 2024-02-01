import requests
import allure
import random
import json
import pytest
from constans import Constants
from faker import Faker

faker = Faker()

class TestOrder:
    @allure.title('Проверка создания заказа')
    @pytest.mark.parametrize("color", ["BLACK", "GREY", "BLACK, GREY", ""])
    def test_create_order(self, color):
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
                    color
                    ]
        }
        payload_string = json.dumps(payload)
        response = requests.post(Constants.url_order, data=payload_string)
        assert "track" in response.text
