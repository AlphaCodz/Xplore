from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    STATUS_CHOICES = (
        ('D', 'Draft'),
        ('P', 'Published'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        )

    gender = models.CharField(max_length= 10, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    middle_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_login}"

