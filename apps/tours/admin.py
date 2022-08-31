from django.contrib import admin
from .models import Tour, Agent, Booking, Package, Review, Activity, TourRequest


# Register your models here.
admin.site.register(Tour)
admin.site.register(Agent)
admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(TourRequest)
admin.site.register(Activity)