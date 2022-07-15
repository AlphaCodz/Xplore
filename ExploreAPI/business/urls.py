from django.urls import path, re_path
# from .views import 
from . import views

urlpatterns = [
    path('customers/', views.CustomerView.as_view(), name='customer'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name="customer-details")
]


