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
    path('pending',views.PendingBookings, name="pending"),
    path('approved', views.ApprovedBookings, name="approved"),
    path('declined', views.DeclinedBookings, name="declined"),
    path('paid', views.PaidBookings, name="paid")
]