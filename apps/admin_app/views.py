from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tours.models import *
from tours.serializers import BookingSerializer, UserDetailSerializer
from django.views.generic import ListView, DetailView

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
@permission_classes([permissions.IsAdminUser])
def detail_counts(request):
    
        pending = Booking.objects.filter(status="P").count()
        approved = Booking.objects.filter(status="A").count()
        declined = Booking.objects.filter(status="D").count()
        paid = Booking.objects.filter(paid = True).count()
        
        # Passing queries as context
        query = {
        "pending": pending,
        "approved": approved,
        "declined": declined,
        "paid": paid,
    }
    
        return JsonResponse(query)

def UserDetailsList(request, id):
   user = Customer.objects.get(id=id)
   details = Booking.objects.all()
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
       "number_of_person": details.individuals
            }
        
        detail_list.append(query)
        context_data = {"detail_list":detail_list}
            
        return JsonResponse(context_data)

    


