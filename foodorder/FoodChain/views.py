from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Dishes,Place,Restorent
# Create your views here.
class DishLstView(ListView):
    model = Dishes
    template_name =''
    context_object_name = 'dishlist'
    def

class PlaceListView(ListView):
    model = Place
    template_name = ''

class RestListView(ListView):
    model = Restorent
    template_name = ''

