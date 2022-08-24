from rest_framework import serializers
from .models import TourAgency
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator
from api.models import Customer



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

class TourAgencySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset= TourAgency.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators =[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = TourAgency
        fields = ("name", "profile_pic", "email", "address", "license", "phone_number" ,"cac", "password", "password2")
        extra_kwargs = {
            "name" : {'required':True},
            "profile_pic" : {'required':False},
            "email" : {'required':True},
            "phone_number": {'required':True},
            "address" : {'required':True},
            "license" : {'required': True},
            "cac" : {'required':True},
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

        Tour_Agency = TourAgency.objects.create(
            customer = customer,
            name = validated_data["name"],
            email = validated_data["email"],
            profile_pic = validated_data["profile_pic"],
            phone_number = validated_data['phone_number'],
            address = validated_data["address"],
            license = validated_data["license"],
            cac = validated_data["cac"]
        )
        
        Tour_Agency.save()
        return Tour_Agency