import requests
import pytest
from constans import Constants


@pytest.fixture(scope='function')
def prepare_courier():
    courier = {
        "login": "jul54",
        "password": "j1992",
        "firstName": "yuliya"
    }
    requests.post(Constants.url_courier, data=courier)
    response = requests.post(Constants.url_authorization, data=courier)
    yield prepare_courier
    id_courier = response.json()['id']
    requests.delete(f"{Constants.url_courier}/{id_courier}")



