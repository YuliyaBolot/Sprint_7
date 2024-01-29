import requests
import allure
import random
import string
from user import User
from faker import Faker

faker = Faker()

class TestAuthorization:
    @allure.title('Курьер может авторизоваться')
    def test_courier_can_log_in(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        first_name = login_pass[2]
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert 200 == response.status_code

    @allure.title('Авторизация с обязательными полями')
    def test_authorization_with_required_field(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert 200 == response.status_code

    @allure.title('Попытка авторизации с некорректным паролем')
    def test_authorization_with_incorrect_password(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации с некорректным логином')
    def test_authorization_with_incorrect_login(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации без логина')
    def test_authorization_without_login(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        password = login_pass[1]
        payload = {
            "login": "",
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        error_message = "Недостаточно данных для входа"
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка авторизации под несуществующим пользователем')
    def test_authorization_non_existent_user(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        error_message = "Учетная запись не найдена"
        assert 404 == response.status_code and error_message in response.text

    @allure.title('Возврат id при успешной авторизации')
    def test_successful_request_return_id(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert "id" in response.text

