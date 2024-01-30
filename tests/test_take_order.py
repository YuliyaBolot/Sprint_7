import random
import requests
import allure
from constans import Constants
from helpers import Helpers
from faker import Faker

faker = Faker()

class TestTakeOrder:
    @allure.title('Проверка получения ответа об успешном принятии заказа')
    def test_take_order(self):
        helper = Helpers()
        order = helper.create_order()
        response = requests.post(Constants.url_order, data=order)
        id_order = response.json()["track"]
        courier = helper.authorization_with_required_fields()
        response_post = requests.post(Constants.url_authorization, data=courier)
        id_courier = response_post.json()['id']
        response_put = requests.put(f"{Constants.url_take_order}{id_order}?courierId={id_courier}")
        assert '{"ok":true}' in response_put.text

    @allure.title('Попытка принять заказ без указания id курьера')
    def test_take_order_without_id_courier(self):
        helper = Helpers()
        order = helper.create_order()
        response_post = requests.post(Constants.url_order, data=order)
        id_order = response_post.json()["track"]
        response_put = requests.put(f"{Constants.url_take_order}{id_order}?courierId=")
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_put.text and 400 == response_put.status_code

    @allure.title('Попытка принять заказ с указанием неверного id курьера')
    def test_take_order_with_incorrect_id_courier(self):
        helper = Helpers()
        order = helper.create_order()
        response_post = requests.post(Constants.url_order, data=order)
        id_order = response_post.json()["track"]
        id_courier = random.randint(1000000, 9999999)
        response_put = requests.put(f"{Constants.url_take_order}{id_order}?courierId={id_courier}")
        error_message = "Курьера с таким id не существует"
        assert error_message in response_put.text and 404 == response_put.status_code

    @allure.title('Попытка принять заказ без указания id заказа')
    def test_take_order_without_id_order(self):
        helper = Helpers()
        courier = helper.authorization_with_required_fields()
        response_post = requests.post(Constants.url_authorization, data=courier)
        id_courier = response_post.json()['id']
        response_put = requests.put(f"{Constants.url_take_order}courierId={id_courier}")
        error_message = "Недостаточно данных для поиска"
        assert error_message in response_put.text and 400 == response_put.status_code

    @allure.title('Попытка принять заказ с указанием неверного id заказа')
    def test_take_order_with_incorrect_id_order(self):
        helper = Helpers()
        courier = helper.authorization_with_required_fields()
        response_post = requests.post(Constants.url_authorization, data=courier)
        id_courier = response_post.json()['id']
        id_order = random.randint(1000000, 9999999)
        response_put = requests.put(f"{Constants.url_take_order}{id_order}?courierId={id_courier}")
        error_message = "Заказа с таким id не существует"
        assert error_message in response_put.text and 404 == response_put.status_code








