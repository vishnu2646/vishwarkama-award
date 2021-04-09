from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views.generic import DetailView
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
# Create your views here.
@login_required(login_url="login")
@allowed_users(allowed_roles=['Patient'])
def index(request):
    doctors = Doctor.objects.all()
    result = Doctor.objects.values('spelization').annotate(the_count=Count('spelization'))
    context = {
        'doctors':doctors,
        'result':result
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
    context = {
        'date':date,
        'doctors':logged_in_user_details
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
    context = {
        'appoinments':appoinments
    }
    return render(request,'appoinments.html',context)

def bookappoinments(request):
    if request.method == "POST":  
        a_form = AppoinmentForm(request.POST,instance=request.user)
        if a_form.is_valid():
            a_form.save()
            messages.success(request, f'Your Appoinment is booked Successfully...')
            return redirect("home")
    else:
        a_form = AppoinmentForm()
    return render(request,'booking.html',{'a_form':a_form})

