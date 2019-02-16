from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Dish, Place, Restorent, DishOrder, DishItem, Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from .forms import OrderCreate, RestCreate, CustomerCreation

from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
class DishLstView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'FoodChain/dish_list.html'
    context_object_name = 'dishlist'

    def get_queryset(self):
        return Dish.objects.all()


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
    model = Dish
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
    listt = DishItem.objects.get(pk=pk).restorent_set.all()
    dishorder = DishOrder()
    userid = request.user.id
    if request.method == 'POST':
        order = OrderCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity = order.cleaned_data['quantity']
            dishorder.dishitem = DishItem.objects.get(pk=pk)
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
    listt = Restorent.objects.get(pk=pk).dishitem_set.all()
    dishorder = DishOrder()
    userid = request.user.id
    if request.method == 'POST':
        order = RestCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity = order.cleaned_data['quantity']
            dishorder.dishitem = order.cleaned_data['dishitem']
            dishorder.restaurent = Restorent.objects.get(pk=pk)
            dishorder.user = User.objects.get(id=userid)
            dishorder.save()
            return render(request, 'FoodChain/user_details.html')
        else:
            return render(request, 'FoodChain/form_ordeer.html', {'form': order})
    else:
        order = RestCreate(list1=listt)
        return render(request, 'FoodChain/form_ordeer.html', {'form': order})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            u = form.cleaned_data.get('username')
            p = form.cleaned_data.get('password1')
            user = authenticate(username=u, password=p)
            user.groups.add(Group.objects.get(name='customers'))
            login(request, user)
            return redirect('foodchain:customercreate', pk=user.id)
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:

        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


@login_required
def homepage(request):
    dlist = Dish.objects.all()[:5]
    rlist = Restorent.objects.all()[:5]
    return render(request, 'FoodChain/home.html', {'di': dlist, 'rest': rlist})


def customerCreate(request, pk):
    cust = Customer()
    if request.method == 'POST':
        form = CustomerCreation(request.POST)
        if form.is_valid():
            cust.DelivaryAddress = form.cleaned_data['DelivaryAddress']
            cust.image = form.cleaned_data['image']
            cust.phono = form.cleaned_data['phono']
            cust.details = User.objects.get(pk=pk)
            cust.save()
            return redirect('foodchain:homein')
        else:
            return render(request, 'FoodChain/customercreate.html', {'form': form})
    else:
        form = CustomerCreation()
        return render(request, 'FoodChain/customercreate.html', {'form': form})
