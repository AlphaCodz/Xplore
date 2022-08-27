from datetime import datetime
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from api.models import Customer
from tours.serializers import AgentSerializer
from .models import TourAgency
from django.http import JsonResponse
from rest_framework import generics, status, authentication, permissions
from tours.models import Tour, Booking, Agent
from tours.serializers import TourSerializer, BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import TourAgencySerializer
import jwt
from config.settings import SECRET_KEY
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# Create your views here.   
class RegisterTourAgency(generics.GenericAPIView):
    serializer_class = TourAgencySerializer
    
    def post(self, request):
        agency = request.data
        serializer = self.serializer_class(data=agency)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        agency_data = serializer.data
        
        return Response(agency_data, status=status.HTTP_201_CREATED)
    
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def AgencyDetails(request, id):
    user = Customer.objects.get(id=id)
    details = TourAgency.objects.filter(customer=user)
    agency_list = []
    for details in details:
        query = {
       "id": details.customer.id,
       "name": details.name,
       "logo": details.logo
        }
        agency_list.append(query)
    context_data = {"Tour_Agency_list":agency_list}         
    return JsonResponse(context_data)

# Add Tour
class AddTour(generics.CreateAPIView):
    
    def post(self, request, format=None):
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    
    # To view all the Tour Lists no matter the id
class TourList(APIView):
    def get(self, request, format=None):
        snippets = Tour.objects.all()
        serializer = TourSerializer(snippets, many=True)
        return Response(serializer.data)

class TourDetail(APIView):
    def get_object(self, pk):
        try:
            return Tour.objects.get(pk=pk)
        except Tour.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        tours = self.get_object(pk)
        serializer = TourSerializer(tours)
        return JsonResponse(serializer.data)

    def put(self, request, pk, format=None):
        tours = self.get_object(pk)
        serializer = TourSerializer(tours, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        tours = self.get_object(pk)
        tours.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def all_bookings(request, status):
    qs = Booking.objects.filter(status=status)
    bookings = []
    for booking in qs:
        json_form = {
            "id": booking.id,
            "customer": str(booking.customer),
            "agent": str(booking.agent),
        }
        bookings.append(json_form)
    data = {status:bookings}
    return JsonResponse(data)


@api_view(["PUT"])
def approve_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = "A"
    booking.save()
    data = BookingSerializer(booking).data
    return Response(data, 200)

@api_view(["PUT"])
def decline_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = "D"
    booking.save()
    data = BookingSerializer(booking).data
    return Response(data, 200)

@csrf_exempt
@authentication_classes([authentication.TokenAuthentication])
def GenerateToken(request):
    user = request.user
    #add agency email to payload
    payload = {
        "timestamp": str(datetime.now()),
        "email": user.email,
    }
    email = request.POST.get("email")
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    host = request.get_host()
    send_mail(
            "Welcome",
            f"welcome \n Click here to create your account http://{host}/api/verify_email/{token}",
            "jenake8@gmail.com",
            [email],
            fail_silently=False,
    ) 
    return JsonResponse({"status":"Success"})

@api_view(["GET"])
def Agents(request, pk):
    agency = TourAgency.objects.get(id=pk)
    details = Agent.objects.filter(tour_agency=agency)
    detail_list = []
    for details in details:
        query = {
            "id": details.first_name
        }
        detail_list.append(query)
    context_data = {"detail_list":detail_list}     
    return JsonResponse(context_data)

class RegisterAgent(generics.CreateAPIView):
    serializer_class = AgentSerializer