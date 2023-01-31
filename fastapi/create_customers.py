import requests
import json
import random
import string
from pprint import pprint

url = "http://127.0.0.1:8000/create_customer"


adjectives = ["Creative", "Innovative", "Dynamic", "Efficient", "Powerful", "Learning", "Cisco", "Tiktok", "Juniper", "AAA", "Company", "Measured", "Cleaning"]
nouns = ["Solutions", "Tech", "Enterprise", "Global", "Group", "Network", "World"]

for i in range(100):
    def generate_random_company_name():
        return random.choice(adjectives) + " " + random.choice(nouns)

    def generate_random_rut():
        characters = string.digits
        result = ''.join(random.choice(characters) for i in range(10))
        return result+"."+random.choice(characters)

    company = generate_random_company_name()
    rut = generate_random_rut()

    payload = json.dumps({
    "customer_name" : company,
    "customer_rut": rut})

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    pprint(response.json())