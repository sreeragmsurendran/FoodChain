
from django.urls import path,include
from .views import *
app_name = 'foodchain'
urlpatterns = [

    path('dishes/', DishLstView.as_view(), name='dishlist'),
    path('places/',PlaceListView.as_view(),name='places'),
    path('restaurent/',RestListView.as_view(),name='restorents'),
    path('dishes/<int:pk>/',DishDetailedView.as_view(),name='dishdetails'),
    path('place/<int:pk>/',PlaceDetailedView.as_view(),name='placedetails'),
    path('restaurent/<int:pk>/',RestDetailedView.as_view(),name='restaurentDetails'),

]
