from rest_framework import serializers
from .models import Tour, Booking, Passport, Agent
import re
from django.contrib.auth.hashers import make_password

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "agency" ,"name", "description", "details", "location", "start_date", "end_date", "image")

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
    
        
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "profile_pic",
            "tour_agency"
                )

