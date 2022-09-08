import jwt
from cryptography.hazmat.primitives import serialization
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.permissions import BasePermission
# from Xplore.apps.touragency.models import TourAgency

# CREATE A TOKEN USING JWT HS256 ALGORITHM
# payload_data = {
#     "sub": "12",
#     "name": "Alpha",
#     "nickname":"Viccy"
# }

# my_secret = "my_super_secret"
# token = jwt.encode (
        
#         payload=payload_data, 
        
#         key=my_secret
#     )
# print(jwt.decode(token, key=my_secret, algorithms=['HS256']))

# today = datetime.today() + relativedelta(days=5)
# print(today)

# class IsAgency(BasePermission):
#     message = "You are not authorized to add a Tour"
#     def has_permission(self, request, view):
#         email = request.user.email
#         agency_mail = TourAgency.objects.get(email=email)
#         if email in agency_mail:
#             return False
#         return True
    

