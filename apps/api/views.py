import email
from .serializers import CustomerSerializer, RegisterSerilizer
from rest_framework import generics, permissions
from .models import Customer
from rest_framework.views import APIView
from rest_framework.response import Response
from api.renderers import CustomRenderer
from .token import generate_token_from_user, validate_token
from django.core.mail import send_mail
from django.http.response import HttpResponse

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
    renderer_classes = [CustomRenderer,]

class CustomerDetail(APIView):
    permission_classes= (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        if request.user:
            serializer = CustomerSerializer(user)
            return Response(serializer.data)

class GenerateToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        host = request.get_host()
        user = request.user
        data = {}
        data["email"] = user.email
        token = generate_token_from_user(data)
        send_mail(
            "Verify Email",
            f"http://{host}/api/verify_email/{token}",
            "bbruks07@gmail.com",
            [user.email],
        )
        return Response({"message": "verification mail sent"})

def verify_email(request, token):
    validation = validate_token(token)
    if validation["status"]:
        user = Customer.objects.get(email=validation["user"]["email"])
        user.verified_email = True
        user.save()
    return HttpResponse(validation["message"])