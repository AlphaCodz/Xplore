from django.db import models
from tours.models import Customer

# Create your models here.

class TourAgency(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, related_name="Agencies")
    
    name = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(upload_to= "media/tour_agency/profile_pic/", blank=True)
    email = models.EmailField(editable=True, unique= True, null=True)
    address = models.CharField(max_length=200, unique=True, editable=True, null=True)
    phone_number = models.BigIntegerField(unique=True, null=True)
    license = models.ImageField(upload_to="media/tour_agency/license/")
    cac = models.ImageField(upload_to="media/tour_agency/CAC/" )
    # payment_info = models.IntegerField( unique=True, null=True)
    
    def get_agency(self):
        return f"Tour Agency: {self.name}"
    
    def __repr__(self):
        return self.name + "is added"
    
    def __str__(self):
        return f"{self.name}"
    
