from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Dishes, Place, Restorent
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DishLstView(LoginRequiredMixin,ListView):
    model = Dishes
    template_name = 'FoodChain/dish_list.html'
    context_object_name = 'dishlist'

    def get_queryset(self):
        return Dishes.objects.all()


class PlaceListView(LoginRequiredMixin,ListView):
    model = Place
    template_name = 'FoodChain/place_list.html'
    context_object_name = 'placelist'

    def get_queryset(self):
        return Place.objects.all()


class RestListView(LoginRequiredMixin,ListView):
    model = Restorent
    template_name = 'FoodChain/restaurent_list.html'
    context_object_name = 'restlist'

    def get_queryset(self):
        return Restorent.objects.all()


class DishDetailedView(LoginRequiredMixin,DetailView):
    model = Dishes
    template_name = 'FoodChain/dish_details.html'
    context_object_name = 'dishd'


class PlaceDetailedView(LoginRequiredMixin,DetailView):
    model = Place
    template_name = 'FoodChain/place_details.html'
    context_object_name = 'placed'


class RestDetailedView(LoginRequiredMixin,DetailView):
    model = Restorent
    template_name = 'FoodChain/restaurent_details.html'
    context_object_name = 'restd'
