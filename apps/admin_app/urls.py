from django.urls import path
from .views import CustomerList

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
]