from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Dish, Place, Restorent, DishOrder, DishItem, Customer, Address, RestaurantOrder
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from .forms import OrderCreate, RestCreate, CustomerCreation, AddressCreate, DishItemCreate,DishItemEdit

from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


# Create your views here.

class DishLstView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'FoodChain.add_dishorder'
    model = Dish
    template_name = 'FoodChain/dish_list.html'
    context_object_name = 'dishlist'

    def get_queryset(self):
        return Dish.objects.all()


class PlaceListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'FoodChain.add_dishorder'
    model = Place
    template_name = 'FoodChain/place_list.html'
    context_object_name = 'placelist'

    def get_queryset(self):
        return Place.objects.all()


class RestListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'FoodChain.add_dishorder'
    model = Restorent
    template_name = 'FoodChain/restaurent_list.html'
    context_object_name = 'restlist'

    def get_queryset(self):
        return Restorent.objects.all()


class DishDetailedView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'FoodChain.add_dishorder'
    model = Dish
    template_name = 'FoodChain/dish_details.html'
    context_object_name = 'dishd'


class PlaceDetailedView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'FoodChain.add_dishorder'
    model = Place
    template_name = 'FoodChain/place_details.html'
    context_object_name = 'placed'


class RestDetailedView(LoginRequiredMixin, DetailView):
    model = Restorent
    template_name = 'FoodChain/restaurent_details.html'
    context_object_name = 'restd'


class CustomerDetailedView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'FoodChain.add_dishorder'
    model = Customer
    template_name = 'FoodChain/user_details.html'
    context_object_name = 'customer'


class RestaurantProfile(PermissionRequiredMixin, DetailView):
    permission_required = 'FoodChain.add_dishitem'
    model = Restorent
    template_name = 'FoodChain/restaurent_profile.html'
    context_object_name = 'restaurant'


@permission_required('FoodChain.add_dishorder')
def order_create(request, pk):
    listt = Dish.objects.get(pk=pk).restorent_set.all()
    dishorder = DishOrder()
    customerid = request.user.customer
    if request.method == 'POST':
        order = OrderCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity = order.cleaned_data['quantity']
            dishorder.dishitem = DishItem.objects.get(pk=pk)
            dishorder.restaurent = order.cleaned_data['restaurent']
            dishorder.customer = customerid
            dishorder.save()
            return render(request, 'FoodChain/user_details.html')
        else:
            return render(request, 'FoodChain/dishcreate.html', {'form': order})
    else:
        order = OrderCreate(list1=listt)
        return render(request, 'FoodChain/dishcreate.html', {'form': order})


@permission_required('FoodChain.add_dishorder')
def rest_create(request, pk):
    listt = Restorent.objects.get(pk=pk).dishitem_set.all()
    dishorder = DishOrder()
    custid = request.user.customer
    if request.method == 'POST':
        order = RestCreate(request.POST, list1=listt)
        if order.is_valid():
            dishorder.quantity = order.cleaned_data['quantity']
            dishorder.dishitem = order.cleaned_data['dishitem']
            dishorder.restaurent = Restorent.objects.get(pk=pk)
            dishorder.customer = custid
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
            user.groups.add(Group.objects.get(name='Customers'))

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
    addobj = Address()
    if request.method == 'POST':
        form = CustomerCreation(request.POST, request.FILES)
        address = AddressCreate(request.POST)
        if form.is_valid() and address.is_valid():
            addobj.district = address.cleaned_data['district']
            addobj.housename = address.cleaned_data['housename']
            addobj.landmark = address.cleaned_data['landmark']
            addobj.pincode = address.cleaned_data['pincode']
            addobj.village = address.cleaned_data['village']
            addobj.save()
            cust.DelivaryAddress = addobj
            cust.image = form.cleaned_data['image']
            cust.phono = form.cleaned_data['phono']
            user = User.objects.get(pk=pk)
            cust.details = user
            login(request, user)
            cust.save()
            return redirect('foodchain:homein')
        else:
            return render(request, 'FoodChain/customercreate.html', {'formc': form, 'forma': address})
    else:
        form = CustomerCreation()
        address = AddressCreate()
        return render(request, 'FoodChain/customercreate.html', {'formc': form, 'forma': address})


@permission_required('FoodChain.add_dishitem')
def dish_item_create(request):
    dishobj = DishItem()
    res = request.user.restorent
    dishlist = res.dish.all()
    if request.method == 'POST':

        form = DishItemCreate(request.POST, list1=dishlist)
        if form.is_valid():
            dishobj.restaurent = res
            dishobj.price = form.cleaned_data['price']
            dishobj.dish = form.cleaned_data['dish']
            dishobj.save()
            return redirect('')
        else:
            return render(request, 'FoodChain/dish_item_create.html', {'form': form})
    else:
        form = DishItemCreate(list1=dishlist)
        return render(request, 'FoodChain/dish_item_create.html', {'form': form})


@permission_required('FoodChain.add_dishitem')
def rest_order_list(request, pk):
    rest = Restorent.objects.get(pk=pk).restaurantorder_set.all()
    return render(request, 'FoodChain/restaurant_order.html', {'list_order': rest})


def rest_item_list(request, pk):
    item = Restorent.objects.get(pk=pk).dishitem_set.all()
    return render(request, 'FoodChain/rest_items_list.html', {'rest_item': item})


def rest_edit_dish(request , pk):

    edit = get_object_or_404(DishItem,pk=pk)
    if request.method == 'POST':
        form =DishItemEdit(request.POST,instance= edit)
        if form.is_valid():
            form.save()
            return redirect('foodchain:restitemlist')
        return render(request,'FoodChain/rest_dish_edit.html',{'form' :form})

