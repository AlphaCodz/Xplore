import email
from urllib.parse import uses_params
from .serializers import CustomerSerializer, RegisterSerilizer
from rest_framework import generics, permissions
from .models import Customer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        page = self.request.GET.get("page")
        if not page:
            page = 1
        start = (page * 100) - 99
        stop =  page * 100
        print(start, stop)
        qs = Customer.objects.all()[start:stop]
        return qs

class RegisterCustomer(generics.CreateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerilizer

class CustomerDetail(APIView):
    permission_classes= (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        if request.user:
            serializer = CustomerSerializer(user)
            return Response(serializer.data)