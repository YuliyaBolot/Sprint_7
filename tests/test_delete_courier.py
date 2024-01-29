import requests
import allure
import random
from user import User

class TestDeleteCourier:
    @allure.title('Проверка сообщения об успешном удалении курьера')
    def test_delete_courier_with_correct_id(self):
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
        response_delete = requests.delete(f"{url}/api/v1/courier/{id_courier}")
        assert '{"ok":true}' in response_delete.text

    @allure.title('Попытка удаления курьера с несуществующим id')
    def test_delete_courier_with_non_existent_id(self):
        url = 'https://qa-scooter.praktikum-services.ru'
        id_courier = random.randint(0, 9999)
        response_delete = requests.delete(f"{url}/api/v1/courier/{id_courier}")
        error_message = "Курьера с таким id нет."
        assert error_message in response_delete.text



