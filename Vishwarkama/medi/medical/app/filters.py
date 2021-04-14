import django_filters
from .models import *
from .forms import * 

class AppoinmentFilters(django_filters.FilterSet):
    class Meta:
        model = Appoinment
        fields = ['doctor_name']

class DoctorFilters(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = ['location','specalization']