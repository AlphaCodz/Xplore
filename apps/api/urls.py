from django.urls import path
from .views import RegisterCustomer, CustomerDetail, GenerateToken, verify_email

urlpatterns = [
    path('register', RegisterCustomer.as_view(), name='register'),
    path('me', CustomerDetail.as_view(), name="me"),
    path('send_email_reset_token', GenerateToken.as_view(), name='generate-token'),
    path('verify_email/<token>', verify_email, name='verify-email'),
]