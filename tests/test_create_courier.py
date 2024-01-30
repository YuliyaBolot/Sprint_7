import requests
import allure
from faker import Faker
from helpers import Helpers
from constans import Constants

faker = Faker()

class TestCourier:

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_create_two_identical_couriers(self, prepare_courier):
        next_courier = {
            "login": "jul54",
            "password": "j1992",
            "firstName": "yuliya"
        }
        response = requests.post(Constants.url_courier, data=next_courier)
        assert 409 == response.status_code

    @allure.title('Проверка, что для создания курьера нужно передать все обязательные поля')
    def test_create_courier_with_required_field(self):
        helper = Helpers()
        payload = {
            "login": helper.create_login_and_password()[0],
            "password": helper.create_login_and_password()[1],
            "firstName": ''
        }
        response = requests.post(Constants.url_courier, data=payload)
        assert 201 == response.status_code

    @allure.title('Проверка получения ответа и верного кода при успешном создании курьера')
    def test_correct_response_code_about_successful_registration(self):
        helper = Helpers()
        payload = {
            "login": helper.create_login_and_password()[0],
            "password": helper.create_login_and_password()[1],
            "firstName": faker.first_name()
        }
        response = requests.post(Constants.url_courier, data=payload)
        success_message = '{"ok":true}'
        assert 201 == response.status_code and success_message in response.text

    @allure.title('Попытка создать курьера без логина')
    def test_create_courier_without_login(self):
        helper = Helpers()
        payload = {
            "login": '',
            "password": helper.create_login_and_password()[1],
            "firstName": faker.first_name()
        }
        response = requests.post(Constants.url_courier, data=payload)
        error_message = 'Недостаточно данных для создания учетной записи'
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка создать курьера без пароля')
    def test_create_courier_without_password(self):
        helper = Helpers()
        payload = {
            "login": helper.create_login_and_password()[0],
            "password": '',
            "firstName": faker.first_name()
        }
        response = requests.post(Constants.url_courier, data=payload)
        error_message = 'Недостаточно данных для создания учетной записи'
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка создать курьера с уже созданным логином')
    def test_create_courier_with_already_existing_login(self, prepare_courier):
        helper = Helpers()
        next_courier = {
            "login": "jul54",
            "password": helper.create_login_and_password()[1],
            "firstName": faker.first_name()
        }
        response = requests.post(Constants.url_courier, data=next_courier)
        error_message = 'Этот логин уже используется. Попробуйте другой.'
        assert error_message in response.text

