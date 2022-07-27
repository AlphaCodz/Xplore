from django.urls import re_path
from . import views

app_name = "webadmin"

urlpatterns = [
    re_path(r'^index/$', views.index, name="index")
]
