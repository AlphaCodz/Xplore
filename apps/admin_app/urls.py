from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('customer/details', views.detail_counts, name="count"),
    path('customer/info/<int:id>',views.UserDetailsList, name='customer_info'),
    path('admin/reg', RegAdmin.as_view(), name='adminreg'),
    path('admin/login', MyTokenObtainPairView.as_view(), name='adminlogin'),
    path('admin/details', AdminDetail.as_view(), name='admindetails'),
    path('pending',views.PendingCustomers, name="pending"),
    path('approved', views.ApprovedCustomers, name="approved"),
    path('declined', views.DeclinedCustomers, name="declined"),
    path('paid', views.PaidCustomers, name="paid")
]