from urllib import request
from rest_framework import serializers
from .models import Activity, Tour, Booking, Passport, Agent, Package, TourRequest
from djmoney.money import Money
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from tours.models import Customer
import re

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "agency" ,"name", "description", "location", "start_date", "end_date", "image")

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
        package = validated_data["package"]
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
    
    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance
    
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
        
class TourRequestSerializer(serializers.ModelSerializer):
    activities = serializers.StringRelatedField(many=True)
    class Meta:
        model = TourRequest
        fields = ("destination", "category", "budget", "start_date", "end_date", "activities",)
    
    def create(self, validated_data):
        expected_activities = ["activity1", "activity2", "activity3"]
        tour_request = TourRequest.objects.create(
            customer = self.context["request"].user,
            destination= validated_data["destination"],
            category = validated_data["category"],
            budget = Money(validated_data["budget"], "NGN"),
            start_date = validated_data["start_date"],
            end_date = validated_data["end_date"],
        )
        tour_request.save()
        for i in expected_activities:
            field = self.context["request"].POST.get(i)
            if field:
                activity = Activity.objects.create(
                    activity = field,
                    tour_request = tour_request
                )
                activity.save()
        return tour_request

class AgentSerializer(serializers.ModelSerializer):  
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset= Agent.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators =[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Agent
        fields = ("first_name", "last_name", "email", "phone_number","address", "profile_pic", "tour_agency", "password", "password2")
        extra_kwargs = {
            "first_name":{'required':True},
            "last_name":{'required':True},
            "email":{'required':True},
            "address":{'required':True},
            "tour_agency": {'required':True},
            "phone_number": {'required':True}            
        }
    def validate(self, attrs):
        pattern = "[^a-z A-Z 0-9]"
        if attrs['password'] != attrs['password2']:
            return "Password Does Not Match!"
        if attrs["password"].islower():
            raise serializers.ValidationError({"password": "Password fields must contain upper and lowercase"})
        if not re.findall(pattern, attrs["password"]):
            raise serializers.ValidationError({"password": "password must contain special character"})
        return attrs
    
    def create(self, validated_data):
        customer = Customer.objects.create(
            email = validated_data['email']
        )
        customer.set_password(raw_password=validated_data['password'])
        customer.save()
        
        Agents = Agent.objects.create(
            first_name=validated_data["first_name"],
            last_name = validated_data["password"],
            email = validated_data["email"],
            phone_number = validated_data["phone_number"],
            address = validated_data["address"],
            profile_pic = validated_data["profile_pic"],
            tour_agency = validated_data["tour_agency"]
        )
        Agents.save()
        return Agents
        