from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tours.models import *
from .serializers import AdminSerializer
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from tours.serializers import BookingSerializer
from django.views.generic import ListView, DetailView
from rest_framework.response import Response


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
# @permission_classes([permissions.IsAdminUser])
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
        "package_type":details.package.package_type,
        "package_price": str(details.package.price),
        "number_of_person": details.individuals,
        "location": details.tour.location
        }
        detail_list.append(query)
    context_data = {"detail_list":detail_list}
            
    return JsonResponse(context_data)


@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
class RegAdmin(generics.CreateAPIView):
    queryset = AdminReg.objects.all()
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = AdminSerializer
        
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
class AdminDetail(APIView):
    permission_classes= (permissions.IsAdminUser,)
    def get(self, request, format=None):
        user = request.user
        if request.user:
            serializer = AdminSerializer(user)
            return Response(serializer.data)
        

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def PendingCustomers(request):
    queryset = Booking.objects.filter(status="P")
    pending_users = []
    
    for pending in queryset:
        query = {
        "customer_id": pending.customer.id,
        "first_name": pending.customer.first_name,
        "last_name": pending.customer.last_name,
        "pending_since": pending.created_at
        }
        pending_users.append(query)
    context_data = {"pending_users":pending_users}
            
    return JsonResponse(context_data)

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def ApprovedCustomers(request):
    queryset = Booking.objects.filter(status="A")
    approved_users = []
    
    for approved in queryset:
        query = {
            "customer_id":approved.customer.id,
            "first_name": approved.customer.first_name,
            "last_name": approved.customer.last_name,
            "approved_since": approved.created_at
        }
        approved_users.append(query)
    context = {
        "approved_users":approved_users
    }
    return JsonResponse(context)
        
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def DeclinedCustomers(request):
    queryset = Booking.objects.filter(status="D")
    declined_users = []
    
    for declined in queryset:
        query = {
          "customer_id":declined.customer.id,
          "first_name":declined.customer.first_name,
          "last_name":declined.customer.last_name,
          "declined_since": declined.created_at  
        }
        declined_users.append(query)
    context = {
        "declined":declined_users
    }
    return JsonResponse(context)

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def PaidCustomers(request):
    queryset = Booking.objects.filter(paid=True)
    paid_users = []
    
    for paid in queryset:
        query = {
            "customer_id":paid.customer.id,
            "first_name": paid.customer.first_name,
            "last_name": paid.customer.last_name,
            "paid_since": paid.created_at
            
        }
        paid_users.append(query)
    data =  {
        "paid": paid_users
    }
    return JsonResponse(data)
    
def Bookingslip(request):
    pass