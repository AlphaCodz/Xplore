from django.urls import re_path, path
from . import views

app_name = "webadmin"

urlpatterns = [
    path('index/', views.index, name="index"),
    path('approved/', views.approved, name="approved"),
    path('decline/', views.declined, name= "declined"),
    path('pending/', views.pending, name="pending" ),
    path('paid/', views.paid, name= "paid")
]
