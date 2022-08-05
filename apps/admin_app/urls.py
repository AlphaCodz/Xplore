from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('customer/details', views.detail_counts, name="count"),
    path('customer/info/<int:id>',views.UserDetailsList, name='customer_info'),
]