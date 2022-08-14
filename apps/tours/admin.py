from django.contrib import admin
from .models import Tour, Agent, Package, Booking, TourAgency


# Register your models here.
admin.site.register(Tour)
admin.site.register(Agent)
admin.site.register(Package)
# admin.site.register(Booking)
# admin.site.register(Admin)
admin.site.register(Booking)
admin.site.register(TourAgency)

