from struct import pack
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Tour, Package, Agent
from .serializers import TourSerializer

# Create your views here.
class TourList(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        qs = Tour.objects.all().order_by("start_date", "end_date")
        return qs

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
