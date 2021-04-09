from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.
CATEGORY_CHOICES = (
    ('IS','In Stock'),
    ('US','Stock Unavalible')
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    label = models.CharField(max_length=2,choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Item", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart",kwargs={"pk":self.pk})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'pk': self.pk
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    appartment_address = models.CharField(max_length=50)
    country = CountryField(multiple=False)
    zipcode = models.CharField(max_length=100)
    phone = models.IntegerField()
    
class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wishlist_item = models.ManyToManyField(Item)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wished_item.title   
    