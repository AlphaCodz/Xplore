from django.contrib import admin
from .models import Tour, Agent, Booking, TourAgency


# Register your models here.
admin.site.register(Tour)
admin.site.register(Agent)
# admin.site.register(Admin)
admin.site.register(Booking)

