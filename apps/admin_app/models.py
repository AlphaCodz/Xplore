from django.db import models
from birthday import BirthdayField, BirthdayManager
from api.models import Customer

# Create your models here.
class AdminReg(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)

    #proxy fields
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)

    staff_number = models.CharField(max_length=6, unique=True, null=True)
    birthday = BirthdayField(null=True)
    home_address = models.CharField(max_length=200, null=True)

    objects = BirthdayManager()
    
    def __str__(self):
        return f"{self.last_name} {self.staff_number}"