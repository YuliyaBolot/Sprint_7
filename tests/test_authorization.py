import requests
import allure
from helpers import Helpers
from constans import Constants
from faker import Faker

faker = Faker()

class TestAuthorization:
    @allure.title('Курьер может авторизоваться')
    def test_courier_can_log_in(self):
        helper = Helpers()
        courier = helper.authorization_with_all_fields()
        response = requests.post(Constants.url_authorization, data=courier)
        assert 200 == response.status_code

    @allure.title('Авторизация с обязательными полями')
    def test_authorization_with_required_fields(self):
        helper = Helpers()
        courier = helper.authorization_with_required_fields()
        response = requests.post(Constants.url_authorization, data=courier)
        assert 200 == response.status_code

    @allure.title('Попытка авторизации с некорректным паролем')
    def test_authorization_with_incorrect_password(self, prepare_courier):
        helper = Helpers()
        payload = {
            "login": "jul54",
            "password": helper.create_login_and_password()[1]
        }
        response = requests.post(Constants.url_authorization, data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации с некорректным логином')
    def test_authorization_with_incorrect_login(self, prepare_courier):
        helper = Helpers()
        payload = {
            "login": helper.create_login_and_password()[0],
            "password": "j1992"
        }
        response = requests.post(Constants.url_authorization, data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации без логина')
    def test_authorization_without_login(self, prepare_courier):
        payload = {
            "login": "",
            "password": "j1992"
        }
        response = requests.post(Constants.url_authorization, data=payload)
        error_message = "Недостаточно данных для входа"
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации под несуществующим пользователем')
    def test_authorization_non_existent_user(self):
        helper = Helpers()
        payload = {
            "login": helper.create_login_and_password()[0],
            "password": helper.create_login_and_password()[1]
        }
        response = requests.post(Constants.url_authorization, data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Возврат id при успешной авторизации')
    def test_successful_request_return_id(self):
        helper = Helpers()
        courier = helper.authorization_with_required_fields()
        response = requests.post(Constants.url_authorization, data=courier)
        assert "id" in response.text

