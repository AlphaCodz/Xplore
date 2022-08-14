from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Tour, Booking, Package, Passport, TourAgency
import re
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "description", "details", "location", "start_date", "end_date", "image")

class BookingSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    package = serializers.StringRelatedField()
    passports = serializers.StringRelatedField(many=True)
    class Meta:
        model = Booking
        fields = (
            "id",
            "category", 
            "agent", 
            "tour", 
            "package", 
            "individuals", 
            "status", 
            "paid", 
            "passports",
            )
        extra_kwargs = {
            'tour': {'required': False},
            'agent': {'required': False},
        }

    def create(self, validated_data):
        request = self.context["request"]
        package_id = request.POST.get("package")
        package = Package.objects.get(id=package_id)
        booking = Booking.objects.create(
            customer = request.user,
            package = package,
            agent = package.agent,
            tour = package.tour,
            category = validated_data["category"],
            individuals = validated_data.get("individuals")
        )
        booking.save()
        files = request.FILES
        expected_passport_files = ["passport1", "passport2", "passport3"]
        for i in expected_passport_files:
            if files.get(i):
                passport = Passport.objects.create(
                    booking = booking,
                    image = files.get(i),
                )
                passport.save()
        return booking
    
class PackageSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField()
    class Meta:
        model = Package
        fields = (
            "id", 
            "name", 
            "flight", 
            "accomondation", 
            "feeding", 
            "package_tour", 
            "airport", 
            "description",
            "take_off_date",
            "return_date",
            "take_off_time",
            "price",
            "agent",
            "description",
            "price",
            )

class TourAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAgency
        fields = ("name", "logo", "email", "address", "license", "cac")
        extra_kwargs = {
            "name":{'required':True},
            "agency_logo":{'required':True},
            "agency_email": {'required':True},
            "address": {'required':True},
            "license": {'required': True}
        }
        
    def create(self, validated_data):
        Tour_Agency = TourAgency.objects.create(
            name = validated_data["name"],
            email = validated_data["email"],
            address = validated_data["address"],
            license = validated_data["license"],
            cac = validated_data["cac"]
        )
        Tour_Agency.save()