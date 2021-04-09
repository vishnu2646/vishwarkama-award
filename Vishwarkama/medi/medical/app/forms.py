from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({
                "placeholder": field.label,
                'class': "form-control",
                'autocomplete':"off"
            }) 

class ProfileUpadteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

class AppoinmentForm(forms.ModelForm):
    class Meta:
        model = Appoinment
        fields = ['doctor_name','name','date','phone','reason']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name in self.fields:
    #         field = self.fields.get(field_name)
    #         self.fields[field_name].widget.attrs.update({
    #             "placeholder": field.label,
    #             'class': "form-control",
    #             'autocomplete':"off"
    #         }) 