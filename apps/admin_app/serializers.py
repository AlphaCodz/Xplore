from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Admin
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
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            customer = customer,
            home_address = validated_data['home_address'],
            birthday = validated_data['birthday'],
            staff_number = validated_data['staff_number']
        )  
        admin.save()
        return admin
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user)
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data