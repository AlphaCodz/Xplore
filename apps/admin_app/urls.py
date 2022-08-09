from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('customer/details', views.detail_counts, name="count"),
    path('customer/<int:id>',views.UserDetailsList, name='customer_info'),
    path('register', RegAdmin.as_view(), name='adminreg'),
    path('login', MyTokenObtainPairView.as_view(), name='adminlogin'),
    path('details', AdminDetail.as_view(), name='admindetails')
]