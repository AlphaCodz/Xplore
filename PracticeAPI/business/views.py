from rest_framework.views import APIView
from .models import Customer
from rest_framework.response import Response
from PracticeAPI.serializers import CustomerSerializer
from rest_framework import status
from functools import wraps
# from business.customFunc import resource_checker

# Create your views here.
class CustomerView(APIView):
    def get(self, request, format=None):
        customers = Customer.objects.all().filter(status ="P")
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # Create an instance of the serializer to request all the entered data from the database
        serializer = CustomerSerializer(data=request.data)
        
        # Check if requested data is valid
        if serializer.is_valid():
            # if it's valid, save the data and present it
            serializer.save()
            # Present a 201 status code to the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # What happens if the data is not valid? 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class CustomerDetailView(APIView):
    
    def resource_checker(model):
        def check_entity(fun):
            @wraps
            def inner_func(*args, **kwargs):
                try:
                    x = fun(*args, **kwargs)
                    return x
                except model.DoesNotExist:
                    return Response({'message': "Not Found"}, status= status.HTTP_204_NO_CONTENT)
        return check_entity  
    
    @resource_checker(Customer)
    def get(self, pk, format= None):
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
        
    @resource_checker(Customer)
    def put(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(Customer, data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @resource_checker(Customer)
    def delete(self, request, pk, format=None):
        customer= Customer.objects.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        