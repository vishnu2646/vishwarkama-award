from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item,Order,OrderItem,Address,Wishlist
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
# Create your views here.
class ItemListView(ListView):
    model = Item
    template_name = 'amado/index.html' 
    context_object_name = 'items'

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

'''
class OrderSummaryView(View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'amado/cart.html',context)
        except:
            messages.warning(self.request,'You Do not have an Active Order')
            return redirect("/")
'''
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

class CheckoutVeiw(LoginRequiredMixin,View):  
    def get(self,*args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user,ordered=False)

def checkout(request):
    return render(request,'amado/checkout.html')

def add_to_wishlist(request,pk):
    '''
    wishlist = Wishlist.objects.get_or_create(user = request.user)
    item = Item.objects.get(pk=pk)
    wishlist.wished_item.push(item)
    wishlist.save()
    '''
    return render(request,'shop.html')