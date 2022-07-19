from dataclasses import fields
from rest_framework import serializers
from .models import Tour

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "description", "details", "location", "start_date", "end_date", "image")
