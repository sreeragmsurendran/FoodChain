
from django.urls import path,include
from .views import *
from django.conf.urls import url
app_name = 'foodchain'
urlpatterns = [

    path('dishes/', DishLstView.as_view(), name='dishlist'),
    path('places/', PlaceListView.as_view(),name='places'),
    path('restaurent/', RestListView.as_view(),name='restorents'),
    path('dishes/<int:pk>/', DishDetailedView.as_view(),name='dishdetails'),
    path('place/<int:pk>/', PlaceDetailedView.as_view(),name='placedetails'),
    path('restaurent/<int:pk>/', RestDetailedView.as_view(),name='restaurentDetails'),
    path('user/<int:pk>/', CustomerDetailedView.as_view(), name='customerdet'),
    path('dishorder/<int:pk>/', order_create, name='dishcreate'),
    path('restorder/<int:pk>/', rest_create, name='restcreate'),
    path('signup/', signup,name='signup1'),
    path('', homepage, name='homein'),
    path('customercreate/<int:pk>', customerCreate, name='customercreate'),
    path('dishitemcreate/', dish_item_create, name='dishitemcreate'),
    path('restaurantprofile/<int:pk>/', RestaurantProfile.as_view(), name='restaurantprofile'),
]

