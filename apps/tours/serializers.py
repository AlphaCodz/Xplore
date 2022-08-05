from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import AdminReg, Tour, Booking, Package, Passport
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
    # visa = serializers.StringRelatedField(many=True, read_only=True)
    passports = serializers.StringRelatedField(many=True)
    customer = serializers.StringRelatedField()
    class Meta:
        model = Booking
        fields = ("id", "customer", "category", "agent", "tour", "package", "individuals", "status", "paid", "passports")
        extra_kwargs = {
            'tour': {'required': False},
            'agent': {'required': False},
            'package': {'required':True},
            'id':{'required':True},
            'individuals': {'required':False},
        }

    def create(self, validated_data):
        request = self.context["request"]
        package_id = int(request.POST.get("package"))
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
        # files = request.FILES
        # expected_passport_files = ["passport1", "passport2", "passport3"]
        # expected_visa_files = ["visa1", "visa2", "visa3"]
        # for i in expected_passport_files:
        #     if files.get(i):
        #         passport = Passport.objects.create(
        #             booking = booking,
        #             image = files.get(i),
        #         )
        #         passport.save()
        # for i in expected_visa_files:
        #     if files.get(i):
        #         visa = Visa.objects.create(
        #             image = files.get(i),
        #             booking = booking,
        #         )
        #         visa.save()
        # return booking
        
class UserDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = ("customer_id", "customer", "category", "no_of_persons_on_tour","payment_reference", "package", "email", "package_type")
        
