from django.http import JsonResponse
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tours.models import *
from .serializers import AdminSerializer, ReasonSerializer
from tours.models import Customer, Booking
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from tours.models import Reason
from .models import Admin
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS

# Create your views here.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    def get_queryset(self):
        page = self.request.GET.get("page")
        if not page:
            page = 1
        start = (page * 100) - 99
        stop =  page * 100
        print(start, stop)
        qs = Customer.objects.all()[start:stop]
        return qs

    
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def detail_counts(request):
    pending = Booking.objects.filter(status="P").count()
    approved = Booking.objects.filter(status="A").count()
    declined = Booking.objects.filter(status="D").count()
    paid = Booking.objects.filter(paid = True).count()

    query = {
        "pending":pending,
        "approved":approved,
        "declined":declined,
        "paid":paid,
    }
    
    return JsonResponse(query)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
@permission_classes([permissions.IsAdminUser])
def UserDetailsList(request, id):
    user = Customer.objects.get(id=id)
    details = Booking.objects.filter(customer=user)
    detail_list = []
    for details in details:
        query = {
        "user_id":details.customer.id,
        "Booking_id":details.id,
        "category": details.category,
        "first_name":details.customer.first_name,
        "last_name":details.customer.last_name,
        "email":details.customer.email,
        "package":details.package,
        "number_of_person": details.individuals,
        "location": details.tour.location
        }
        detail_list.append(query)
    context_data = {"detail_list":detail_list}
            
    return JsonResponse(context_data)


class RegisterAdmin(generics.CreateAPIView):
    queryset = Admin.objects.all()
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = AdminSerializer
        

class AdminDetail(APIView):
    permission_classes= (permissions.IsAdminUser,)
    def get(self, request, format=None):
        user = request.user
        if request.user:
            serializer = AdminSerializer(user)
            return Response(serializer.data)
        
class ReasonFor(generics.CreateAPIView):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    permission_classes = (permissions.IsAdminUser,)
    
        
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


# Register as Tour Agency
