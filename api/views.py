import email
from .serializers import CustomerSerializer, RegisterSerilizer
from rest_framework import generics, permissions
from .models import Customer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

class RegisterCustomer(generics.CreateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerilizer

@csrf_exempt
def register_customer(request):
    if request.method == "POST":
        formdata = request.POST
        required = []
        if not formdata.get("first_name"):
            required.append("first_name is required")

        errors = []
        if Customer.objects.get(email= formdata["email"]):
            errors.append("this email is already registered")
        

        res = {}
        return JsonResponse(res)
    else:
        return JsonResponse({"detail": "method not allowed"}, status=405)