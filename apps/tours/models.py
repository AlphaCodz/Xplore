from email.policy import default
from django.db import models
from api.models import Customer
from djmoney.models.fields import MoneyField

# Create your models here.
class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    details = models.TextField()
    location = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    image = models.ImageField(upload_to="tours/%y/%m/%d/", null=True)
    def __str__(self):
        return self.name

class Agent(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="agents/", null=True)
    def __str__(self):
        return self.name

class Package(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    flight = models.CharField(max_length=20, null=True)
    accomondation = models.CharField(max_length=20, null=True)
    feeding = models.CharField(max_length=20, null=True)
    package_tour = models.CharField(max_length=20, null=True)
    airport = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    take_off_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    take_off_time = models.DateTimeField(null=True)
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="NGN", null=True)
    def __str__(self):
        return f"{self.name}"

class Guide(models.Model):
    name = models.CharField(max_length=50)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="guides/", null=True)
    
    def __str__(self):
        return f"Company: {self.agent} ____ Guide: {self.name}"

class Booking(models.Model):
    CATEGORY_CHOICES = (
        ("S", "single"),
        ("C", "couple"),
        ("M", "multiple")
    )

    STATUS_CHOICES = (
        ("P", "pending"),
        ("A", "approved"),
        ("D", "declined"),
    )
    INDIVIDUAL_CHOICES = (
        (3, 3),
        (4, 4),
        (5, 5),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name="customer")
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    individuals = models.IntegerField(choices=INDIVIDUAL_CHOICES, null=True)
    paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="P")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.customer} {self.status}"

class Visa(models.Model):
    image = models.ImageField(upload_to="visa/%y/%m/%d/")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="visa")
    def __str__(self):
        return f"/media/{self.image}"

class Passport(models.Model):
    image = models.ImageField(upload_to="passport/%y/%m/%d/")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="passports")
    def __str__(self):
        return f"/media/{self.image}"