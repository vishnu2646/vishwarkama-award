from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({
                "placeholder": field.label,
                'class': "input-control",
                'autocomplete':"off"
            })

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'123 Main Street',
        'class':'form-control'
    }))
    appartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'Appartment or Suite (optional)',
        'class':'form-control'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Zip Code',
        'class':'form-control'
    }))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'Phone Number',
        'class':'form-control'
    }))
