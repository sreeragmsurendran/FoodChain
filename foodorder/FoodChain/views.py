from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Dishes, Place, Restorent, DishOrder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import OrderCreate, RestCreate


# Create your views here.
class DishLstView(LoginRequiredMixin, ListView):
    model = Dishes
    template_name = 'FoodChain/dish_list.html'
    context_object_name = 'dishlist'

    def get_queryset(self):
        return Dishes.objects.all()


class PlaceListView(LoginRequiredMixin, ListView):
    model = Place
    template_name = 'FoodChain/place_list.html'
    context_object_name = 'placelist'

    def get_queryset(self):
        return Place.objects.all()


class RestListView(LoginRequiredMixin, ListView):
    model = Restorent
    template_name = 'FoodChain/restaurent_list.html'
    context_object_name = 'restlist'

    def get_queryset(self):
        return Restorent.objects.all()


class DishDetailedView(LoginRequiredMixin, DetailView):
    model = Dishes
    template_name = 'FoodChain/dish_details.html'
    context_object_name = 'dishd'


class PlaceDetailedView(LoginRequiredMixin, DetailView):
    model = Place
    template_name = 'FoodChain/place_details.html'
    context_object_name = 'placed'


class RestDetailedView(LoginRequiredMixin, DetailView):
    model = Restorent
    template_name = 'FoodChain/restaurent_details.html'
    context_object_name = 'restd'


class UserpDetailedView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'FoodChain/user_details.html'
    context_object_name = 'userp'


'''class DishOrderCreate(CreateView):
    model = DishOrder
    template_name = 'FoodChain/dishcreate.html'
    form_class = OrderCreate

    def get_context_data(self, **kwargs):
        context = super(self).get_context_data(**kwargs)
        context['obj'] =self.kwargs.get('pk')
        return context'''


def order_create(request, pk):
    listt = Dishes.objects.get(pk=pk).restorent_set.all()
    dishorder = DishOrder()
    userid = request.user.id
    if request.method == 'POST':
        order = OrderCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity = order.cleaned_data['quantity']
            dishorder.dish = Dishes.objects.get(pk=pk)
            dishorder.restaurent = order.cleaned_data['restaurent']
            dishorder.user = User.objects.get(id=userid)
            dishorder.save()
            return render(request, 'FoodChain/user_details.html')
        else:
            return render(request, 'FoodChain/dishcreate.html', {'form': order})
    else:
        order = OrderCreate(list1=listt)
        return render(request, 'FoodChain/dishcreate.html', {'form': order})


def rest_create(request, pk):
    listt = Restorent.objects.get(pk=pk).dishes.all()
    dishorder = DishOrder()
    userid = request.user.id
    if request.method == 'POST':
        order = RestCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity= order.cleaned_data['quantity']
            dishorder.dish = order.cleaned_data['dish']
            dishorder.restaurent = Restorent.objects.get(pk=pk)
            dishorder.user = User.objects.get(id=userid)
            dishorder.save()
            return render(request, 'FoodChain/user_details.html')
        else:
            return render(request, 'FoodChain/form_ordeer.html', {'form': order})
    else:
        order = RestCreate(list1=listt)
        return render(request, 'FoodChain/form_ordeer.html', {'form': order})
