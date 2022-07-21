from django.contrib import admin
from .models import Tour, Agent, Package, Guide

# Register your models here.
admin.site.register(Tour)
admin.site.register(Agent)
admin.site.register(Package)
admin.site.register(Guide)