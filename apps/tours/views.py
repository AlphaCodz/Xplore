from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from requests import request
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Tour, Booking
from .serializers import TourSerializer, BookingSerializer
from .payment import Paystack
from rest_framework import filters

class DetailBookingPermission(permissions.BasePermission):
    message = "you are not permitted to view this document"
    def has_permission(self, request, view):
        return view.get_object().customer == request.user

class MustBeCustomerBooking(permissions.BasePermission):
    message = "This booking doesnt belong to this customer"
    def has_permission(self, request, view):
        pk = request.resolver_match.kwargs.get("pk")
        booking = get_object_or_404(Booking, pk=pk)
        return request.user == booking.customer 

class TourList(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        qs = Tour.objects.all().order_by("start_date", "end_date")
        return qs

class BookTour(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

def tourPackageList(request, id):
    tour = Tour.objects.get(id=id)
    packages = Package.objects.filter(tour=tour)
    package_list = []

    for package in packages:
        package_json = {
            "id": package.id,
            "name": package.name,
            "flight": package.flight,
            "accomondation": package.accomondation,
            "feeding": package.feeding,
            "package_tour": package.package_tour,
            "airport": package.airport,
            "description": package.description,
            "take_off_date": package.take_off_date,
            "return_date": package.return_date,
            "take_off_time": package.take_off_time,
            "price": str(package.price),
            "agent": package.agent.name,
            "agent_logo": str(package.agent.logo),
            "description": package.description,
        }
        package_list.append(package_json)

    data = {"packages": package_list}
    return JsonResponse(data)

"""class TourPackageList(generics.ListAPIView):
    serializer_class = PackageSerializer
    def get_queryset(self):
        tour = get_object_or_404(Tour, pk=self.kwargs.get("id"))
        packages = Package.objects.filter(tour = tour)
        return packages"""

class BookingList(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        qs = Booking.objects.filter(customer= self.request.user).prefetch_related("agent", "tour", "package").order_by("-id")
        return qs

class BookingDetail(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = (DetailBookingPermission, permissions.IsAuthenticated)

    def get_queryset(self):
        qs = get_object_or_404(Booking, pk= self.kwargs.get("pk"))
        return qs
    
    def get_object(self):
        qs = self.get_queryset()
        return qs

class SubmitPayment(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    def get_queryset(self):
        qs = get_object_or_404(Booking, pk= self.kwargs.get("pk"))
        print(qs)
        return qs
    
    def put(self, request, *args, **kwargs):
        obj = self.get_queryset()
        data = BookingSerializer(obj)
        refrence = self.request.POST.get("reference")
        print(refrence)
        P = Paystack()
        status = P.verify_transaction(refrence)["data"]["status"]
        print(status)
        if status == "success":
            obj.paid == True
            obj.save()
        return Response(data.data)
    
class TourSearchList(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name', '^location']