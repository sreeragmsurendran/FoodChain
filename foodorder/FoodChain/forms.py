from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import DishOrder, Dish, Restorent, Customer, Address, DishItem


class OrderCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk1 = kwargs.pop('list1')

        super(OrderCreate, self).__init__(*args, **kwargs)
        self.fields['restaurent'] = forms.ModelChoiceField(queryset=pk1)

    class Meta:
        model = DishOrder
        fields = (
            'quantity',
            'restaurent',
        )


class CustomerCreation(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'image',
            'phono',
        )


class RestCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk1 = kwargs.pop('list1')

        super(RestCreate, self).__init__(*args, **kwargs)
        self.fields['dishitem'] = forms.ModelChoiceField(queryset=pk1)

    class Meta:
        model = DishOrder
        fields = (
            'quantity',
            'dishitem',
        )


class AddressCreate(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class DishItemCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk1 = kwargs.pop('list1')

        super(DishItemCreate, self).__init__(*args, **kwargs)
        self.fields['dish'] = forms.ModelChoiceField(queryset=pk1)

    class Meta:
        model = DishItem
        fields = (
            'price',
            'dish',
        )

class DishItemEdit(forms.ModelForm):
    class Meta:
        model= DishItem
        fields =(
            'name',
            'price',
            'status',
    )
class DishItemAdd(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk1 = kwargs.pop('listd')

        super(DishItemAdd, self).__init__(*args, **kwargs)
        self.fields['dish'] = forms.ModelChoiceField(queryset=pk1)

    class Meta:
        model = DishItem
        fields = (
            'price',
            'dish',
            'status',
        )