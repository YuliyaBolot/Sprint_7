import random
import string
import json
from user import User
from faker import Faker

faker = Faker()

class Helpers:
    def authorization_with_all_fields(self):
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
        return payload

    def authorization_with_required_fields(self):
        user = User()
        login_pass = user.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        return payload

    def create_order(self):
        payload = {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "address": faker.street_address(),
            "metroStation": random.randint(0, 333),
            "phone": faker.phone_number(),
            "rentTime": random.randint(0, 7),
            "deliveryDate": f"2024-02-{random.randint(1, 29)}",
            "comment": "Please leave at the gates",
            "color": [
                "BLACK"
            ]
        }
        payload_string = json.dumps(payload)
        return payload_string

    def create_login_and_password(self):
        log_pas = []
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        log_pas.append(login)
        log_pas.append(password)
        return log_pas
