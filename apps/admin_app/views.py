from django.http import JsonResponse
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions

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