from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput

from . models import *

# Create your views here.
class BrandsForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Brand Name'}),
        }

class ProductForm(forms.ModelForm):

    status = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ['brand','name','starp_color','highlights','price','stock','status','image']

        widgets = {
            'brand': Select(attrs={'class': 'select2 form-control mb-3 custom-select','placeholder' : 'Enter Brand'}),
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'starp_color': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Strap Color'}),
            'highlights': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Highlights'}),
            'price': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Price'}),
            'stock': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Stock'}),
            'status': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Status'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
            raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file