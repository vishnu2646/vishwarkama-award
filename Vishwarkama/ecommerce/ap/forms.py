from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('C', 'COD')
)

class CheckoutForm(forms.ModelForm):
    name = forms.CharField(required=True)
    comany = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    shipping_address = forms.CharField(required=True)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)
    phone = forms.IntegerField()
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
