import requests
import allure
import random
from helpers import Helpers
from constans import Constants

class TestDeleteCourier:
    @allure.title('Проверка сообщения об успешном удалении курьера')
    def test_delete_courier_with_correct_id(self):
        helper = Helpers()
        courier = helper.authorization_with_required_fields()
        response_post = requests.post(Constants.url_authorization, data=courier)
        id_courier = response_post.json()['id']
        response_delete = requests.delete(f"{Constants.url_courier}/{id_courier}")
        assert '{"ok":true}' in response_delete.text

    @allure.title('Попытка удаления курьера с несуществующим id')
    def test_delete_courier_with_non_existent_id(self):
        id_courier = random.randint(1000000, 9999999)
        response_delete = requests.delete(f"{Constants.url_courier}/{id_courier}")
        error_message = "Курьера с таким id нет."
        assert error_message in response_delete.text



