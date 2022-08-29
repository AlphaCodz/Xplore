from tracemalloc import start
from rest_framework import serializers
from touragency.models import TourAgency
from .models import Activity, Tour, Booking, Passport, Agent, Package, TourRequest
from djmoney.money import Money
import jwt
from config.settings import SECRET_KEY
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "agency" , "description", "location", "start_date", "end_date", "image")
    
    def validate(self, attrs):
        
        # Convert dt to string
        starting_date = "{}".format(attrs["start_date"])
        end_date = "{}".format(attrs["end_date"])
        
        # Specify the format of dt display
        starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        two_days_time = datetime.today() + relativedelta(days=2)
        
        if starting_date < two_days_time:
            raise serializers.ValidationError({"date error": "Tours dates must be set to at least 2 days after creation time"})
        if end_date < two_days_time:
            raise serializers.ValidationError({"date error": "Tours dates must be set to at least 2 days after creation time"})
        if attrs["name"].islower():
            raise serializers.ValidationError({"name case error": "Tour name fields must contain uppercase and lowercase characters"})
        return attrs  
    
    def create(self, validated_data):
        tour = Tour.objects.create(
            agency = validated_data["agency"],
            name = validated_data["name"],
            description = validated_data["description"],
            location = validated_data["location"],
            start_date = validated_data["start_date"],
            end_date = validated_data["end_date"],
            image = validated_data["image"]
        )
        tour.save()
        return tour
    
class BookingSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    package = serializers.StringRelatedField()
    passports = serializers.StringRelatedField(many=True)    
    class Meta:
        model = Booking
        fields = (
            "id",
            "category", 
            "agent", 
            "tour", 
            "package", 
            "individuals", 
            "status", 
            "paid", 
            "passports",
            )
        extra_kwargs = {
            'tour': {'required': False},
            'agent': {'required': False},
        }

    def create(self, validated_data):
        request = self.context["request"]
        package = validated_data["package"]
        booking = Booking.objects.create(
            customer = request.user,
            package = package,
            agent = package.agent,
            tour = package.tour,
            category = validated_data["category"],
            individuals = validated_data.get("individuals")
        )
        booking.save()
        files = request.FILES
        expected_passport_files = ["passport1", "passport2", "passport3"]
        for i in expected_passport_files:
            if files.get(i):
                passport = Passport.objects.create(
                    booking = booking,
                    image = files.get(i),
                )
                passport.save()
        return booking
    
    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance
    
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = (
            "id", 
            "tour",
            "name", 
            "flight", 
            "accomodation", 
            "feeding", 
            "airport", 
            "description",
            "take_off_date",
            "return_date",
            "take_off_time",
            "price"
)
    
    def validate(self, attrs):
        # Convert take off datetime object to str
        take_off_date = "{}".format(attrs["take_off_date"])
        take_off_date = datetime.strptime(take_off_date, '%Y-%m-%d')
        
        # Add 5 days to creation days
        two_days_time = datetime.today() + relativedelta(days=2)
        
        if take_off_date < two_days_time:
            raise serializers.ValidationError({"take_off_date error": "Tours dates must be set to at least 2 days after creation time"})
        return attrs
        
    def create(self, validated_data):
        packages = Package.objects.create(
            tour = validated_data["tour"],
            name = validated_data["name"],
            flight = validated_data["flight"],
            accomodation = validated_data["accomodation"],
            feeding = validated_data["feeding"],
            airport = validated_data["airport"],
            description = validated_data["description"],
            take_off_date = validated_data["take_off_date"],
            return_date = validated_data["return_date"],
            take_off_time = validated_data["take_off_time"],
            price = validated_data["price"],
            )
        packages.save()
        return packages
        
class AgentSerializer(serializers.ModelSerializer):
    tour_agency = serializers.StringRelatedField()
    class Meta:
        model = Agent
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "profile_pic",
            "tour_agency"
                )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
    def validate(self, attrs):
        token = self.context["request"].parser_context["kwargs"]["token"]
        #check if token is valid
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            self.decoded_token = decoded_token
        except:
            raise serializers.ValidationError({"token":"invalid token"})
        #check if token is expired
        time_stamp = decoded_token["timestamp"]
        
        #convert timestamp from string to datetime object
        time_stamp = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S.%f')
        time_stamp += timedelta(minutes=5)
        if time_stamp > datetime.now():
            raise serializers.ValidationError({"token":"expired token"})
        return attrs
    
    def create(self, validated_data):
        print(self.decoded_token)
        agency = TourAgency.objects.get(email=self.decoded_token["agency_email"])
        agent = Agent.objects.create(
            first_name= validated_data["first_name"],
            last_name = validated_data["last_name"],
            phone_number = validated_data.get("phone_number"),
            address = validated_data.get("address"),
            profile_pic = validated_data.get("profile_pic"),
            tour_agency = agency,
        )
        return agent

class TourRequestSerializer(serializers.ModelSerializer):
    activities = serializers.StringRelatedField(many=True)
    class Meta:
        model = TourRequest
        fields = ("destination", "category", "budget", "start_date", "end_date", "activities",)
    
    def create(self, validated_data):
        expected_activities = ["activity1", "activity2", "activity3"]
        tour_request = TourRequest.objects.create(
            customer = self.context["request"].user,
            destination= validated_data["destination"],
            category = validated_data["category"],
            budget = Money(validated_data["budget"], "NGN"),
            start_date = validated_data["start_date"],
            end_date = validated_data["end_date"],
        )
        tour_request.save()
        for i in expected_activities:
            field = self.context["request"].POST.get(i)
            if field:
                activity = Activity.objects.create(
                    activity = field,
                    tour_request = tour_request
                )
                activity.save()
        return tour_request