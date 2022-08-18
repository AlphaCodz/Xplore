from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from api.models import Customer
from .models import TourAgency
from django.http import JsonResponse
from .serializers import TourAgencySerializer, MyTokenObtainPairSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterTourAgency(generics.CreateAPIView):
    queryset = TourAgency.objects.all()
    serializer_class = TourAgencySerializer
    

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