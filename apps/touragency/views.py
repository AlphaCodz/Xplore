from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from api.models import Customer
from .models import TourAgency
from django.http import JsonResponse
from .serializers import TourAgencySerializer, MyTokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from tours.models import Tour, Agent, Booking
from tours.serializers import TourSerializer
from rest_framework.views import APIView
from tours.serializers import TourSerializer, AgentSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import filters

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
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
@permission_classes([permissions.IsAuthenticated])
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # To view all the Tour Lists no matter the id
class TourList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Tour.objects.all()
        serializer = TourSerializer(snippets, many=True)
        return Response(serializer.data)

class TourDetail(APIView):
    """
   get, update or delete a tour.
   Note that the get works by id so id must be specified
    """
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
            "booking_id": booking.id,
            "customer": str(booking.customer),
            "Assigned Tour Agent": str(booking.agent),
            "From": str(booking.agent.tour_agency)

        }
        bookings.append(json_form)
    data = {status:bookings}
    return JsonResponse(data)