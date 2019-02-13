from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import DishOrder, Dishes, Restorent


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


class UserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        var = kwargs.pop('list1')
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=var)


class RestCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk1 = kwargs.pop('list1')

        super(RestCreate, self).__init__(*args, **kwargs)
        self.fields['dish'] = forms.ModelChoiceField(queryset=pk1)

    class Meta:
        model = DishOrder
        fields = (
            'quantity',
            'dish',
        )
