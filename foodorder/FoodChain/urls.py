
from django.urls import path,include
from .views import *
urlpatterns = [

    path('dishes/', DishLstView.as_view(), name='dishlist'),
    path('places/',PlaceListView.as_view(),name='places'),
    path('restaurent/',RestListView.as_view(),name='restorents'),
    path('<int:pk>',DishDetailedView.as_view(),name='dishdetails'),
    path('placedetails/',PlaceDetailedView.as_view(),name='placedetails'),
    path('restaurentdetails/',RestDetailedView.as_view(),name='restaurentDetails'),
]
