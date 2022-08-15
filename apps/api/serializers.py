from django.forms import CharField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Customer
import re
from django.core.mail import send_mail

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "middle_name", "email", "gender", "status", "phone_number")

class RegisterSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset= Customer.objects.all())]
    )
    phone_number = PhoneNumberField(
        required = True,
        validators = [UniqueValidator(queryset= Customer.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators =[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Customer
        fields = ("id", 'password', 'password2', 'email', 'first_name', 'last_name', 'phone_number',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        pattern = "[^a-z A-Z 0-9]"
       
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs["password"].islower():
            raise serializers.ValidationError({"password": "Password fields must contain upper and lowercase"})
        if not re.findall(pattern, attrs["password"]):
            raise serializers.ValidationError({"password": "password must contain special character"})
        return attrs
    
    def create(self, validated_data):
        customer = Customer.objects.create(
            email=validated_data['email'],
            username= validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )  
        customer.set_password(raw_password = validated_data['password'])
        customer.save()
        send_mail(
            "Welcome",
            "welcome",
            "jenake8@gmail.com",
            [validated_data["email"]],
            fail_silently=False,
        )
        return customer 