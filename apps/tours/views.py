from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Tour, Package, Agent, Booking, Passport
from .serializers import TourSerializer, BookingSerializer
from .payment import Paystack

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
            "price": package.price,
            "agent": package.agent.name,
            "agent_logo": str(package.agent.logo),
            "description": package.description,
        }
        package_list.append(package_json)

    data = {"packages": package_list}
    return JsonResponse(data)

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
        qs = Booking.objects.get(id= self.kwargs["pk"])
        return qs
    
    def get_object(self):
        qs = self.get_queryset()
        return qs

@api_view(["post"])
@permission_classes([MustBeCustomerBooking])
def pay(request, pk):
    data = {}
    return Response(data)

class PayForBooking(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (DetailBookingPermission,)
    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(Booking, pk=pk)
    
    def put(self, request, *args, **kwargs):
        P = Paystack()
        user = request.user
        booking = self.get_object()
        if not booking.payment_reference:
            amount = booking.package.price * 100
            email = user.email
            try:
                payment = P.initialize_payment(amount, email)
            except:
                return Response({
                    "detail": "Some error occured"
                },502)
            authorization_url = payment["data"]["authorization_url"]
            reference = payment["data"]["reference"]
            data = {
                "authorization_url": authorization_url,
                "reference": reference,
            }
            booking.payment_reference = reference
            booking.save()
            return Response(data)
        else:
            data = P.verify_transaction(booking.payment_reference)
            if data["data"]["status"] == "success":
                booking.paid = True
                booking.save()
                return Response({
                    "details":"Paid",
                })
            
            else:
                booking.payment_reference = None
                booking.save()
                amount = booking.package.price * 100
                email = user.email
                try:
                    payment = P.initialize_payment(amount, email)
                except:
                    return Response({
                        "detail": "Some error occured"
                    },502)
                authorization_url = payment["data"]["authorization_url"]
                reference = payment["data"]["reference"]
                data = {
                    "authorization_url": authorization_url,
                    "reference": reference,
                }
                booking.payment_reference = reference
                booking.save()
                return Response(data)
