from django.urls import path
from .views import CustomerList, count_bookings

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('count', count_bookings, name='count'),
]