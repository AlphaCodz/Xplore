from django.shortcuts import render
from tours.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from tours.models import Booking
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def index(request):
    pending = Booking.objects.filter(status="P").count()
    approved = Booking.objects.filter(status="A").count()
    declined = Booking.objects.filter(status="D").count()
    paid = Booking.objects.filter(paid = True).count()
    query = Booking.objects.filter(status="P").prefetch_related("customer")

    context = {
        "pending": pending,
        "approved": approved,
        "declined": declined,
        "paid": paid,
        "query":query,
    }
    return render(request, 'index.html', context)


# @api_view(["GET"])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# @permission_classes([permissions.IsAdminUser])
"""def userinfo(request):
    query = Booking.objects.filter(status="P").prefetch_related("customer")
    #  Booking.objects.filter(paid=True)
    context = {
        "query": query,
    }
    
    return render(request, 'index.html', context)""" 