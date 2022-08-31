#from sys import addaudithook, maxsize
from django.db import models
from api.models import Customer
from admin_app.models import Admin
from djmoney.models.fields import MoneyField
from touragency.models import TourAgency
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tour(models.Model):
    agency = models.ForeignKey(TourAgency, on_delete= models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    image = models.ImageField(upload_to="tours/%y/%m/%d/", null=True)
    auto_approve = models.BooleanField(default=False)
    
    def get_tour(self):
        return f"Tour: {self.name}" 
    
    def __str__(self):
        return self.name

class Agent(models.Model):
    tour_agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True) 
    email = models.EmailField(null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = PhoneNumberField(null=True)
    address = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to ="agents/profile_pic/", null=True)
    password = models.CharField(max_length=20, null=True)
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Review(models.Model):
    rating = models.IntegerField()
    review = models.TextField(null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.rating)
    
    class Meta:
        indexes = [models.Index(fields = ["content_type", "object_id"])]



class Package(models.Model):
    TYPE_CHOICES = (
        ("R", "Regular"),
        ("V","VIP"),
        ("VV","VVIP")
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default="R", null=True)
    flight = models.CharField(max_length=20, null=True)
    accomodation = models.CharField(max_length=20, null=True)
    feeding = models.CharField(max_length=20, null=True)
    airport = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    take_off_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    take_off_time = models.DateTimeField(null=True)
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="NGN", null=True)
    ratings = GenericRelation(Review)
    #agent = models.OneToOneField(Agent, on_delete=models.PROTECT, null=True)
    
    def __str__(self):
        return f"{self.name}"

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name="customer")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    individuals = models.IntegerField(null=True, default = 1)
    paid = models.BooleanField(default=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    payment_reference = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    approved_by = models.ForeignKey(Admin, on_delete=models.PROTECT, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.customer} {self.status}"
    
    
    
class Passport(models.Model):
    image = models.ImageField(upload_to="passport/%y/%m/%d/")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="passports")
    def __str__(self):
        return f"/media/{self.image}"
    
class Reason(models.Model):
    REASON_CHOICES = (
        ('IMAGE_NOT_CLEAR', "SUBMITTED IMAGES ARE NOT CLEAR ENOUGH"),
        ('FAKE_DOCUMENT', "DOCUMENTS ARE SUSPECTED TO BE FAKE"),
        ('USER_DETAILS_CONFLICT', "SOME DETAILS ARE NOT CORRECT OR CORRESPONDING")
    )
     
    reason = models.CharField(max_length=50, choices= REASON_CHOICES, null=True)
    other_reasons = models.TextField(max_length=300, null=True)

class TourRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    destination = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    budget = MoneyField(max_digits=19, decimal_places=4, default_currency="NGN", null=True)
    start_date = models.DateField()
    end_date = models.DateField()

class Activity(models.Model):
    activity = models.TextField()
    tour_request = models.ForeignKey(TourRequest, on_delete=models.CASCADE, related_name="activities")
    def __str__(self):
        return self.activity