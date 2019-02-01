from django.contrib import admin

# Register your models here.
from .models import Dishes,Restorent,Place
admin.site.register(Dishes)
admin.site.register(Restorent)
admin.site.register(Place)
