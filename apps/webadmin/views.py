from django.shortcuts import render
from tours.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from tours.models import Booking
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here. INDEX PAGE
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def index(request):
    pending = Booking.objects.filter(status="P").count()
    approved = Booking.objects.filter(status="A").count()
    declined = Booking.objects.filter(status="D").count()
    paid = Booking.objects.filter(paid = True).count()
    query = Booking.objects.filter(status="P").prefetch_related("customer")
    approved_names = Booking.objects.filter(status="A").prefetch_related("customer")
    declined_names = Booking.objects.filter(status="D").prefetch_related("customer")
    context = {
        "pending": pending,
        "approved": approved,
        "declined": declined,
        "approved_names":approved_names,
        "declined_names":declined_names,
        "paid": paid,
        "query":query,
    }
    return render(request, 'index.html', context)
                    
                    # APPROVED PAGE

@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def approved(request):
    approved = Booking.objects.filter(status="A").prefetch_related("customer")
    
    context = {
        "approved": approved,
        "navbar":"approved"
    }
    return render(request, "approved.html", context)

                                        # DECLINED PAGE
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])

def declined(request):
    declined = Booking.objects.filter(status="D").prefetch_related("customer")
    declined_count = Booking.objects.filter(status="D").count()
    
    context = {
        "declined": declined,
        "declined_count":declined_count
    }
    return render(request, 'declined.html', context)

                                         # PAID PAGE

@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def paid(request):
    paid = Booking.objects.filter(paid=True).prefetch_related("customer")
    
    context = {
        "paid": paid,
    }
    return render(request, "paid.html", context)



                            #  PENDING PAGE
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def pending(request):

    pending = Booking.objects.filter(status="P").prefetch_related("customer")
    context = {
        "pending": pending,
    }
    return render(request, 'pending.html', context)

                    # DETAILS PAGE
                    
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def details(request):
    # IF USER HAS PAID, GET THE USER ID, AND GET THE USER DEETAILS BY ID
    paid = Booking.objects.filter(paid=True).prefetch_related("customer")
    
    context = {
        "paid": paid,
    }
    
    return render(request, "details.html", context)



                        # PENDING DETAILS PAGE
@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def pending_details(request):
    
    return render(request, "pending-details.html")


                        # LOGIN USER
@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAdminUser])
def login(request):
    
    return render(request, "login.html")