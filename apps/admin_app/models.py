from django.db import models
from birthday import BirthdayField, BirthdayManager

# Create your models here.
class AdminReg(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    staff_no = models.CharField(max_length=6, unique=True)
    birthday = BirthdayField(null=True)
    home_address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    
    objects = BirthdayManager()
    
    def __str__(self):
        return f"{self.last_name} {self.staff_no}"