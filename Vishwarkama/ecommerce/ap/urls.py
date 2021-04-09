from django.urls import path
from ap.views import ItemListView,ItemDetailView,summary#OrderSummaryView
from . import views

urlpatterns = [
    path('',ItemListView.as_view(),name="home"),
    path('details/<int:pk>/',ItemDetailView.as_view(),name="item-detail"),
    path('add-to-cart/<int:pk>/',views.addtocart,name="add-to-cart"),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pk>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/',summary.as_view(), name='order-summary'),
    path('checkout/',views.checkout,name="checkout"),
    path('wishlist/',views.add_to_wishlist,name="wishlist"),
]