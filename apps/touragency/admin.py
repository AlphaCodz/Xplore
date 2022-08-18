from django.contrib import admin
from .models import TourAgency
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

admin.site.register(TourAgency)