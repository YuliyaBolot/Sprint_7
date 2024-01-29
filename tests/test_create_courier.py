import requests
import allure
import random
import string
from faker import Faker
from user import User

faker = Faker()

class TestCourier:
    @allure.title('Проверка, что курьера можно создать')
    def test_register_new_courier(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        assert len(login_pass) == 3

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_create_two_identical_couriers(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        first_name = login_pass[2]
        user_1 = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=user_1)
        assert 409 == response.status_code

    @allure.title('Проверка, что для создания курьера нужно передать все обязательные поля')
    def test_create_courier_with_required_field(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        first_name = ''
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert 201 == response.status_code

    @allure.title('Проверка возврата верного кода ответа при успешном создании курьера')
    def test_correct_response_code_about_successful_registration(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        first_name = faker.first_name()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert 201 == response.status_code

    @allure.title('Проверка получения ответа при успешном создании курьера')
    def test_response_about_successful_registration(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        first_name = faker.first_name()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert '{"ok":true}' in response.text

    @allure.title('Попытка создать курьера без логина')
    def test_create_courier_without_login(self):
        login = ''
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        first_name = faker.first_name()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        error_message = 'Недостаточно данных для создания учетной записи'
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка создать курьера без пароля')
    def test_create_courier_without_password(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''
        first_name = faker.first_name()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        error_message = 'Недостаточно данных для создания учетной записи'
        assert 400 == response.status_code and error_message in response.text

    @allure.title('Попытка создать курьера с уже созданным логином')
    def test_create_courier_with_already_existing_login(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = faker.password()
        first_name = faker.first_name()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        error_message = 'Этот логин уже используется. Попробуйте другой.'
        assert error_message in response.text

