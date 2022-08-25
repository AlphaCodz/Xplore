from urllib import request
from rest_framework import serializers
from .models import Activity, Tour, Booking, Passport, Agent, Package, TourRequest
from djmoney.money import Money

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