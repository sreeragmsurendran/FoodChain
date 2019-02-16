from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import DishOrder, Dish, Restorent, Customer


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
        fields =(
            'DelivaryAddress',
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
