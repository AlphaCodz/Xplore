from django.urls import path
from .views import CustomerList, RegisterCustomer, CustomerDetail

urlpatterns = [
    path('register', RegisterCustomer.as_view(), name='register'),
    path('me', CustomerDetail.as_view(), name="me"),
]