from django.http import JsonResponse
from django.shortcuts import render
from api.models import Customer
from api.serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from tours.models import Booking
from rest_framework.decorators import permission_classes, api_view

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
@permission_classes([permissions.IsAdminUser])
def count_bookings(request):
    pending = Booking.objects.filter(status="P").count()
    approved = Booking.objects.filter(status="A").count()
    declined = Booking.objects.filter(status="D").count()
    paid = Booking.objects.filter(paid = True).count()

    data = {
        "pending": pending,
        "approved": approved,
        "declined": declined,
        "paid": paid,
    }

    return Response(data)
