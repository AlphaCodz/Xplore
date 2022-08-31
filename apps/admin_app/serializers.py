from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Admin
from tours.models import Reason
import re
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.validators import UniqueValidator
from api.models import Customer

class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset= Customer.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators =[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Admin
        fields = ("first_name", "last_name", "email", "staff_number", "home_address", "password", "password2", "birthday")
        extra_kwargs = {
            "first_name": {'required':True},
            "last_name": {'required':True},
            "email": {'required':True},
            "home_address": {'required':True},
            "birthday": {"required":True},
        }
    
    def validate(self, attrs):
        pattern = "[^a-z A-Z 0-9]"
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs["password"].islower():
            raise serializers.ValidationError({"password": "Password fields must contain upper and lowercase"})
        if not re.findall(pattern, attrs["password"]):
            raise serializers.ValidationError({"password": "password must contain special character"})
        if attrs["password"] == attrs["staff_number"]:
            raise serializers.ValidationError({"password": "Password too common"})
        return attrs  
    
    def create(self, validated_data):
        customer = Customer.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        customer.password = make_password(validated_data['password'])
        customer.save()
        admin = Admin.objects.create(
            customer = customer,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            home_address = validated_data['home_address'],
            birthday = validated_data['birthday'],
            staff_number = validated_data['staff_number']
        )  
        admin.save()
        return admin
                        
                                        # Test Reason serializers  
class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ("reason", "other_reasons")
        extra_kwargs = {
            "reason": {"required":False},
            "other_reasons": {"required":False}
        }
        def validate(self, attrs):
            if attrs["reason"] == attrs["other_reasons"]:
                raise serializers.ValidationError({"reason": "Can't use same reasons"})
            return attrs
        
        def create(self, validated_data):
            reason = Reason.objects.all(
                reason = validated_data["reason"],
                other_reasons = validated_data["other_reasons"]
            )
            reason.save()
            return reason

