from django.contrib import admin

# Register your models here.
from .models import Dishes,Restorent,Place,Address,DishOrder
admin.site.register(Dishes)
admin.site.register(Restorent)
admin.site.register(Place)
admin.site.register(Address)
# admin.site.register(UserProfile)
admin.site.register(DishOrder)


