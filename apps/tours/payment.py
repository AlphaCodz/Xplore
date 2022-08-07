import requests
#import environ

#env = environ.Env()
#environ.Env.read_env()

class Paystack:
    def __init__(self):
        self.headers = {
            'Authorization': 'Bearer sk_test_1f65cbffdf8a332557c6f6f8545fd36a11054c19',
        }
        pass
    def initialize_payment(self, amount, email):
        url = "https://api.paystack.co/transaction/initialize"
        payload={
            'amount': amount,
            'email': email
            }
        response = requests.request("POST", url, headers=self.headers, data=payload)
        return response.json()
    
    def verify_transaction(self, reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=self.headers)
        return response.json()

        

p = Paystack()
print(p.initialize_payment(10000, "bbruks07@gmail.com"))