from django.contrib import admin

# Register your models here.
from .models import Dish,Restorent,Place,Address,DishOrder,DishItem, Customer, RestaurantOrder
admin.site.register(Dish)
admin.site.register(Restorent)
admin.site.register(Place)
admin.site.register(Address)
admin.site.register(DishItem)
admin.site.register(DishOrder)
admin.site.register(Customer)
admin.site.register(RestaurantOrder)

