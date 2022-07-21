from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    details = models.TextField()
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
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
    price = models.BigIntegerField(null=True)
    def __str__(self):
        return f"{self.agent}: {self.tour}"

class Guide(models.Model):
    name = models.CharField(max_length=50)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="guides/", null=True)