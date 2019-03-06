from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Dish, Place, Restorent, DishOrder, DishItem, Customer, Address, RestaurantOrder
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from .forms import OrderCreate, RestCreate, CustomerCreation, AddressCreate, DishItemCreate, DishItemEdit, \
    RestEditProfile, UserEditProfile

from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
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
    template_name = 'FoodChain/rest_profile.html'
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
            return redirect('foodchain:customerdet', pk=dishorder.customer.pk)
        else:
            return render(request, 'FoodChain/dishcreate.html', {'form': order})
    else:
        order = OrderCreate(list1=listt)
        return render(request, 'FoodChain/dishcreate.html', {'form': order})


@permission_required('FoodChain.add_dishorder')
def rest_create(request, pk):
    listt = Restorent.objects.get(r_id=pk).dishitem_set.all()
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
            return redirect('foodchain:customerdet', pk=dishorder.customer.pk)
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


# @permission_required('FoodChain.add_dishitem')
# def dish_item_create(request):
#     if request.method == 'POST':
#         item = DishItem()
#         form = DishItemCreate(request.POST)
#         if form.is_valid():
#             form.save()
#             item.dish = form.cleaned_data.get('dish')
#             item.price = form.cleaned_data.get('price')
#             item.name = form.cleaned_data.get('name')
#             item.restaurent = request.user.restorent
#             item.save()
#             return redirect('foodchain:restitemlist', pk=request.user.restorent.pk)
#         else:
#             return render(request, 'FoodChain/dish_item_create.html', {'form ': form})
#     else:
#         form = DishItemCreate()
#         return render(request,'FoodChain/dish_item_create.html', {'form ': form})
@permission_required('FoodChain.add_dishitem')
def rest_order_list(request, pk):
    rest = Restorent.objects.get(pk=pk).restaurantorder_set.all()
    return render(request, 'FoodChain/restaurant_order.html', {'list_order': rest})


@permission_required('FoodChain.add_dishitem')
def rest_item_list(request, pk):
    item = Restorent.objects.get(pk=pk).dishitem_set.all()
    return render(request, 'FoodChain/rest_items_list.html', {'rest_item': item})


@permission_required('FoodChain.add_dishitem')
def rest_edit_dish(request, pk):
    edit = get_object_or_404(DishItem, id=pk)
    form = DishItemEdit(request.POST or None, instance=edit)
    if form.is_valid():
        form.save()
        return redirect('foodchain:restitemlist', pk=edit.restaurent.pk)
    return render(request, 'FoodChain/rest_dish_edit.html', {'form': form})


def deleteorder(request, pk):
    obj = get_object_or_404(DishOrder, O_id=pk)
    cust = obj.customer.id
    obj.delete()
    return redirect('foodchain:customerdet', pk=cust)


@permission_required('FoodChain.add_dishitem')
def dish_item_add(request):
    if request.method == 'POST':
        item = DishItem()
        form = DishItemCreate(request.POST)
        if form.is_valid():
            item.dish = form.cleaned_data.get('dish')
            item.price = form.cleaned_data.get('price')
            item.name = form.cleaned_data.get('name')
            item.restaurent = request.user.restorent
            item.save()
            return redirect('foodchain:restitemlist', pk=request.user.restorent.pk)
        else:
            return render(request, 'FoodChain/dish_item_create.html', {'form': form})
    else:
        form = DishItemCreate()
        return render(request, 'FoodChain/dish_item_create.html', {'form': form})


@permission_required('FoodChain.add_dishitem')
def rest_edit_profile(request, pk):
    edit = get_object_or_404(Restorent, pk=pk)
    form = RestEditProfile(request.POST or None, instance=edit)
    if form.is_valid():
        form.save()
        return redirect('foodchain:restaurantprofile', pk=edit.pk)
    return render(request, 'FoodChain/rest_edit_profile.html', {'form': form})


@permission_required('FoodChain.add_dishorder')
def cust_edit_profile(request, pk):
    edit = get_object_or_404(Customer, pk=pk)
    form = UserEditProfile(request.POST or None, instance=edit)
    form1 = AddressCreate(request.POST or None, instance=edit.DelivaryAddress)
    if form.is_valid() and form1.is_valid():
        form.save()
        return redirect('foodchain:customerdet', pk=edit.pk)
    return render(request, 'FoodChain/customer_edit_profile.html', {'form': form, 'form1': form1})


class DishItemDetail(generic.DetailView):
    model = DishItem
    context_object_name = 'dish_item'
    template_name = 'FoodChain/dish_item_details.html'
