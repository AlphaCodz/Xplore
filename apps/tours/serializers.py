from dataclasses import fields
from rest_framework import serializers
from .models import Tour, Booking, Package

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "description", "details", "location", "start_date", "end_date", "image")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "category", "agent", "tour", "category")
        extra_kwargs = {
            'tour': {'required': False},
        }

    def create(self, validated_data):
        request = self.context["request"]
        package_id = int(request.POST.get("package_id"))
        package = Package.objects.get(id=package_id)
        booking = Booking.objects.create(
            customer = request.user,
            package = package,
            agent = package.agent,
            tour = package.tour,
            category = validated_data["category"],
        )
        booking.save()
        return booking