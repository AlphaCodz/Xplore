from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customers'),
    path('customer/details', views.detail_counts, name="count"),
    path('customer/info/<int:id>',views.UserDetailsList, name='customer_info'),
    path('admin/reg', RegisterAdmin.as_view(), name='adminreg'),
    path('admin/details', AdminDetail.as_view(), name='admindetails'),
    path('reason', ReasonFor.as_view(), name="reason"),
    path('all-bookings/<status>', views.all_bookings, name='all-bookings'),
]