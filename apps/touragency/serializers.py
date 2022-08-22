from rest_framework import serializers
from .models import TourAgency
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



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
    class Meta:
        model = TourAgency
        fields = ("name", "profile_pic", "email", "address", "license", "cac")
        extra_kwargs = {
            "name" : {'required':True},
            "profile_pic" : {'required':False},
            "email" : {'required':True},
            "address" : {'required':True},
            "license" : {'required': True},
            "cac" : {'required':True}
        }
        
    def create(self, validated_data):
        Tour_Agency = TourAgency.objects.create(
            name = validated_data["name"],
            email = validated_data["email"],
            profile_pic = validated_data["profile_pic"],
            address = validated_data["address"],
            license = validated_data["license"],
            cac = validated_data["cac"]
        )
        Tour_Agency.save()
        return Tour_Agency