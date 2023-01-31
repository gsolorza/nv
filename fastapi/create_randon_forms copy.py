import requests
import json
import random
import string
from pprint import pprint

url = "http://127.0.0.1:8000/create_form"

for i in range(50):
    cm_list = ["Marcelo", "rodo", "PreSales"]
    random_cm = random.choice(cm_list)

    customer_id = [1, 2, 3, 4]
    random_customer = random.choice(customer_id)

    def generate_random_sales_force_id():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(15))

    def generate_random_quote():
        characters = string.digits
        return ''.join(random.choice(characters) for i in range(15))

    random_sf = generate_random_sales_force_id()
    random_quote = generate_random_quote()

    payload = json.dumps({
    "client_manager_name": "George",
    "comments": "[{\"name\": \"admin\", \"role\": \"admin\", \"date\": \"2023-01-27\", \"comment\": \"sdbhvsdijvklsdom,vsdkpjnmvsd l\"}]",
    "customer_id": random_customer,
    "pre_sales_name": random_cm,
    "quote_direct": random_quote,
    "sales_force_id": random_sf,
    "status": "PreSales",
    "dispatch_address": "testing31",
    "customer_address": "sasdasjdbajskdbks1",
    "customer_contact_name": "Jose Jimenez1",
    "customer_contact_phone": "9581453631",
    "customer_contact_email": "j@test.com1",
    "dispatch_receiver_name": "testing31",
    "dispatch_receiver_phone": "9581453631",
    "dispatch_receiver_email": "j@test.com1"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    pprint(response.json())