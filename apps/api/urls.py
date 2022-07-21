from django.urls import path
from .views import CustomerList, RegisterCustomer, register_customer

urlpatterns = [
    path('register', RegisterCustomer.as_view(), name='register'),
]