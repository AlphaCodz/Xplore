from django.http import JsonResponse
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tours.models import Customer, Booking
from .serializers import AdminSerializer
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .models import Admin


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
        "package_type":details.package.package_type,
        "package_price": str(details.package.price),
        "number_of_person": details.individuals,
        "location": details.tour.location
        }
        detail_list.append(query)
    context_data = {"detail_list":detail_list}
            
    return JsonResponse(context_data)


class RegAdmin(generics.CreateAPIView):
    queryset = Admin.objects.all()
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = AdminSerializer
        
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
class AdminDetail(APIView):
    permission_classes= (permissions.IsAdminUser,)
    def get(self, request, format=None):
        user = request.user
        if request.user:
            serializer = AdminSerializer(user)
            return Response(serializer.data)
        
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def PendingBookings(request):
    queryset = Booking.objects.filter(status="P")
    pending_bookings = []
    
    for pending in queryset:
        query = {
        "customer_id": pending.customer.id,
        "first_name": pending.customer.first_name,
        "last_name": pending.customer.last_name,
        "pending_since": pending.created_at
        }
        pending_bookings.append(query)
    context_data = {"pending_users":pending_bookings}
            
    return JsonResponse(context_data)

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def ApprovedBookings(request):
    queryset = Booking.objects.filter(status="A")
    approved_bookings = []
    
    for approved in queryset:
        query = {
            "customer_id":approved.customer.id,
            "first_name": approved.customer.first_name,
            "last_name": approved.customer.last_name,
            "approved_since": approved.created_at
        }
        approved_bookings.append(query)
    context = {
        "approved_users":approved_bookings
    }
    return JsonResponse(context)

@api_view(["GET"])   
@permission_classes([permissions.IsAdminUser])     
def DeclinedBookings(request):
    queryset = Booking.objects.filter(status="D")
    declined_bookings = []
    
    for declined in queryset:
        query = {
          "customer_id":declined.customer.id,
          "first_name":declined.customer.first_name,
          "last_name":declined.customer.last_name,
          "declined_since": declined.created_at,  
          "reason_for_decline": declined.reason,
          "other_reasons": declined.other_reasons
        }
        declined_bookings.append(query)
    context = {
        "declined":declined_bookings
    }
    return JsonResponse(context)

@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def PaidBookings(request):
    queryset = Booking.objects.filter(paid=True)
    paid_bookings = []
    
    for bookings in paid_bookings:
        query = {
            "booking_id":bookings.id,
            "customer": bookings.customer,
        }
        paid_bookings.append(query)
    data =  {
        "paid": paid_bookings
    }
    return JsonResponse(data)

@api_view(["GET"])
def all_bookings(request, status):
    choice_map = {
        "D":"declined",
        "P":"pending",
        "A":"approved",
    }
    qs = Booking.objects.filter(status = status)
    bookings = []
    for booking in qs:
        json_form = {
            "booking_id": booking.id,
            "customer": str(booking.customer),
        }
        bookings.append(json_form)
    data = {choice_map[status]:bookings}
    return JsonResponse(data)