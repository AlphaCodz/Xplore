import jwt
from cryptography.hazmat.primitives import serialization
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


# CREATE A TOKEN USING JWT HS256 ALGORITHM
payload_data = {
    "sub": "12",
    "name": "Alpha",
    "nickname":"Viccy"
}

my_secret = "my_super_secret"
token = jwt.encode (
        
        payload=payload_data, 
        
        key=my_secret
    )
print(jwt.decode(token, key=my_secret, algorithms=['HS256']))



# HOW TO GENERATE A JWT TOKEN USING CRYPTOGRAPHY
# private_key = open('.ssh/id_rsa', 'r').read()
# key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

# new_token = jwt.encode(
#     payload_data= payload_data,
#     key=key,
#     algorithm = 'RS256'
# )
# print(new_token)

today = datetime.today() + relativedelta(days=5)
