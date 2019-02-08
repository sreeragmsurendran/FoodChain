from django import forms

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
