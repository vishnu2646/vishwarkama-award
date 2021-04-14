from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views.generic import DetailView,ListView,CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import date
import datetime
from .decorators import allowed_users,unauthenticated_user,admin_only
from django.db.models import Count
from .filters import * 
from datetime import date
from django.contrib import auth
# Create your views here.
@login_required(login_url="login")
@allowed_users(allowed_roles=['Patient'])
def index(request):
    doctors = Doctor.objects.all()
    result = Doctor.objects.values('specalization').annotate(the_count=Count('specalization'))
    doctor_filter = DoctorFilters(request.GET,queryset=doctors)
    doctors = doctor_filter.qs
    context = {
        'doctors':doctors,
        'result':result,
        'doctor_filter':doctor_filter
    }
    return render(request,'index.html',context)

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'dprofile.html'

def checkout(request):
    return render(request,'checkout.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save()
            user = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request,'An Account was Creates for '+ user)
            return redirect("login")
    context = {
        'form':form
    }
    return render(request,'accounts/doctor-register.html',context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is Wrong")
    return render(request,'accounts/login.html')

def dlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('doctor-home')
        else:
             messages.info(request,"Username or Password is Wrong")
    return render(request,'accounts/doctor-login.html')
        

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
#@admin_only
@allowed_users(allowed_roles=['Doctor'])
def Doctorhome(request):
    date = datetime.date.today()
    logged_in_user_details = Doctor.objects.filter(doctor=request.user)
    tottal_appinments = Appoinment.objects.count()
    doctor_appoinments = Appoinment.objects.values('doctor_name').annotate(appoinments=Count('doctor_name'))
    for doctor_appoinment in doctor_appoinments:
        print(doctor_appoinment)
    context = {
        'date':date,
        'doctors':logged_in_user_details,
        'tottal_appinments':tottal_appinments
    }
    return render(request,'doctor-home.html',context)

@login_required
def Doctorprofile(request):
    logged_in_user_details = Doctor.objects.filter(doctor=request.user)
    if request.method == "POST":
        profile_form =ProfileUpadteForm(request.POST,request.FILES,instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('doctor-profile')
    else:
        profile_form = ProfileUpadteForm(instance=request.user.profile)
    context = {
        'doctors':logged_in_user_details,
        'profile_form':profile_form
    }
    return render(request,'dprofile-settings.html',context)

def appoinments(request):
    appoinments = Appoinment.objects.all()
    filters = AppoinmentFilters(request.GET,queryset=appoinments)
    appoinments = filters.qs
    context = {
        'appoinments':appoinments,
        'filters':filters
    }
    return render(request,'appoinments.html',context)

def bookappoinments(request):
    if request.method == "GET":
        form = AppoinmentForm()
        return render(request,'booking.html',{'form':form})
    if request.method == "POST":
        user = request.user
        appoinment = Appoinment()
        appoinment.user = user
        doctor_int_id = request.POST.get('doctor_name')
        appoinment.doctor_name = Doctor.objects.get(id=doctor_int_id)
        appoinment.name = request.POST.get('name')
        appoinment.date = request.POST.get('date')
        appoinment.phone = request.POST.get('phone')
        appoinment.reason = request.POST.get('reason')
        appoinment.save()
        return redirect('home')

# class AppoinmentCreateView(CreateView):
#     model = Appoinment
#     fields = '__all__'
#     template_name = 'booking.html'
    