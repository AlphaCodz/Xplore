from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('customer/details', views.detail_counts, name="count"),
    path('customer/info/<int:id>',views.UserDetailsList, name='customer_info'),
    path('admin/reg', RegAdmin.as_view(), name='adminreg'),
    path('admin/login', MyTokenObtainPairView.as_view(), name='adminlogin'),
    path('admin/details', AdminDetails.as_view(), name='admindetails')
]

# ALL URLS WORKING FINE