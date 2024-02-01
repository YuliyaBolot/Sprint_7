import requests
import allure
from constans import Constants

class TestOrderList:
    @allure.title('Получение списка заказов')
    def test_get_order_list(self):
        response = requests.get(Constants.url_order)
        r = response.json()
        assert "orders" in r
        