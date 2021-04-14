from django.urls import path
from .views import ItemListView,ItemDetailView,summary,CheckoutVeiw
from . import views

urlpatterns = [
    path('home/',ItemListView.as_view(),name="home"),
    path('details/<int:pk>/',ItemDetailView.as_view(),name="item-detail"),
    path('add-to-cart/<int:pk>/',views.addtocart,name="add-to-cart"),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pk>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/',summary.as_view(), name='order-summary'),
    path('checkout/',CheckoutVeiw.as_view(),name="checkout"),
    path('search/',views.search,name="search"),
    # path('wishlist/',views.add_to_wishlist,name="wishlist"),
    # accounts
    path('',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logoutUser,name='logout'),
]