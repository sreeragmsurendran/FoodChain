from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Dishes,Place,Restorent
# Create your views here.
class DishLstView(ListView):
    model = Dishes
    template_name ='dishesl.html'
    context_object_name = 'dishlist'
    def get_queryset(self):
        return Dishes.objects.all()

class PlaceListView(ListView):
    model = Place
    template_name = ''
    context_object_name = 'placelist'
    def get_queryset(self):
        return Place.objects.all()

class RestListView(ListView):
    model = Restorent
    template_name = ''
    context_object_name = 'restlist'
    def get_queryset(self):
        return Restorent.objects.all()
class DishDetailedView(DetailView):
    model = Dishes
    template_name = ''
    context_object_name = 'dishd'

class PlaceDetailedView(DetailView):
    model = Place
    template_name = ''
    context_object_name = 'placed'

class RestDetailedView(DetailView):
    model = Restorent
    template_name = ''
    context_object_name = 'restd'
