from dataclasses import fields
from rest_framework import serializers
from .models import Tour, Booking, Package, Visa, Passport

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "description", "details", "location", "start_date", "end_date", "image")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "category", "agent", "tour", "package", "individuals")
        extra_kwargs = {
            'tour': {'required': False},
            'agent': {'required': False},
            'package': {'required':False}
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
            individuals = int(validated_data["individuals"])
        )
        booking.save()
        files = request.FILES
        expected_passport_files = ["passport1", "passport2", "passport3"]
        expected_visa_files = ["visa1", "visa2", "visa3"]
        for i in expected_passport_files:
            if files.get(i):
                passport = Passport.objects.create(
                    booking = booking,
                    image = files.get(i),
                )
                passport.save()
        for i in expected_visa_files:
            if files.get(i):
                visa = Visa.objects.create(
                    image = files.get(i),
                    booking = booking,
                )
                visa.save()
        return booking