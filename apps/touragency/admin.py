from django.contrib import admin
from .models import TourAgency
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Register your models here.
# class UserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name')

# class MyUserAdmin(EmailUserAdmin):
#     list_display = ('email', 'is_admin')
#     list_filter = ('is_admin')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_staff', 'is_superuser', 'user_permissions')}),
        
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Custom info', {'fields': ('date_of_birth',)}),
        
    
#     )
    
# admin.site.unregister(get_user_model())
# admin.site.register(get_user_model(), MyUserAdmin)