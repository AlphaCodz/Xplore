from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from django.contrib.auth.models import User



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
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