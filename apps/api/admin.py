from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class UserCreateForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ("email", "first_name", "last_name")

class UserAdmin(UserAdmin):
    add_form = UserCreateForm

# Register your models here.

admin.site.register(Customer, UserAdmin)