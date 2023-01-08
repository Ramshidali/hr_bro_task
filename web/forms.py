from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput
from django import forms

from customer.models import CustomerAddress


class CustomerAddressForm(forms.ModelForm):

    class Meta:
        model = CustomerAddress
        fields = ['name','phone','pincode','locality','address','city','state']

        widgets = {
            'name' :  TextInput(attrs={'class': 'form-control'}),
            'phone' :  TextInput(attrs={'class': 'form-control'}),
            'pincode' :  TextInput(attrs={'class': 'form-control'}),
            'locality' :  TextInput(attrs={'class': 'form-control'}),
            'address' :  Textarea(attrs={'class': 'form-control'}),
            'city' :  TextInput(attrs={'class': 'form-control'}),
            'state' :  TextInput(attrs={'class': 'form-control'}),
        }