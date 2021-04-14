from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,logout,login as auth_login
from .forms import *
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item,Order,OrderItem,Address
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .filters import *

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            return redirect('login')
    context = {
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
            
			user = authenticate(request, username=username, password=password)

			if user is not None:
				auth_login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context = {}
		return render(request, 'accounts/login.html', context) 

def logoutUser(request):
    logout(request)
    return redirect('login')

class ItemListView(ListView):
    model = Item
    template_name = 'amado/index.html' 
    context_object_name = 'items'

    def get_queryset(self):
        qs = self.model.objects.all()
        item_filtered_list = ItemFilter(self.request.GET, queryset=qs)
        print(item_filtered_list)
        return item_filtered_list.qs

class ItemDetailView(DetailView):
    model = Item
    template_name = 'amado/product-details.html'

    
@login_required
def addtocart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"This Item quantity is Updated.")
            return redirect("/order-summary",pk=pk)
        else:
            messages.info(request,"This Item is Added to your cart.")
            order.items.add(order_item)
            return redirect("/order-summary",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request,"This Item quantity is Updated.")
        return redirect("/order-summary",pk=pk)

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary", pk=pk)

class summary(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            }
        except ObjectDoesNotExist:
            return redirect("/")
        return render(self.request,'amado/cart.html',context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutVeiw(LoginRequiredMixin,View):  
    def get(self,*args, **kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request,"amado/checkout.html",context)

    def post(self,*args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address  = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                zipcode = form.cleaned_data.get('zipcode')
                phone = form.cleaned_data.get('phone')
                payment_option = form.cleaned_data.get('payment_option')
                order.save()
                messages.success(self.request,"success")
                return redirect("home")
            return redirect('checkout')
        except ObjectDoesNotExist:
            return redirect("checkout")

def search(request):
    items = Item.objects.all()
    myFilter = ItemFilter(request.GET,queryset=items)
    items = myFilter.qs
    context = {
        'myFilter':myFilter,
        'items':items
    }
    return render(request,'amado/search.html',context)