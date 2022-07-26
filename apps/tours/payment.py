import requests
import environ

env = environ.Env()
environ.Env.read_env()
print(env("test"))



class Paystack:
    def __init__(self):
        pass
    def initialize_payment(self, amount, email):
        url = "https://api.paystack.co/transaction/initialize"
        payload={
            'amount': amount,
            'email': email
            }
        headers = {
            'Authorization': 'Bearer sk_test_1f65cbffdf8a332557c6f6f8545fd36a11054c19',
        }
        response = requests.request("POST", url, headers=headers, data=payload,)
        return response.json()

p = Paystack()
#print(p.initialize_payment("20000", "jenake8@gmail.com"))