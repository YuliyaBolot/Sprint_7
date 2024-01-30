import random
import allure
import requests
from constans import Constants
from helpers import Helpers
from faker import Faker

faker = Faker()

class TestTakeOrder:
    @allure.title('Проверка получения заказа при успешном запросе')
    def test_get_order_by_number(self):
        helper = Helpers()
        order = helper.create_order()
        response_post = requests.post(Constants.url_order, data=order)
        id_order = response_post.json()["track"]
        response_get = requests.get(f"{Constants.url_orders_number}{id_order}")
        assert "order" in response_get.text and 200 == response_get.status_code

    @allure.title('Попытка получить заказ без номера')
    def test_get_order_without_number(self):
        response_get = requests.get(Constants.url_orders_number)
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_get.text

    @allure.title('Попытка получить заказ по несуществующему номеру')
    def test_get_order_with_non_existent_number(self):
        id_order = random.randint(1000000, 9999999)
        response_get = requests.get(f"{Constants.url_orders_number}{id_order}")
        error_message = "Заказ не найден"
        assert error_message in response_get.text


