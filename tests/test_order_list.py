import requests
import allure

class TestOrderList:
    @allure.title('Получение списка заказов')
    def test_get_order_list(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
        r = response.json()
        assert "orders" in r
        