from django.urls import path 
from . import views
from .views import (
    DoctorDetailView,
)

urlpatterns = [
    path('',views.index,name="home"),
    path('dprofile/<int:pk>/',DoctorDetailView.as_view(),name="dprofile"),
    path('doctor-home/',views.Doctorhome,name="doctor-home"),
    path('doctor-profile/',views.Doctorprofile,name="doctor-profile"),
    # accounts
    path('login/',views.login,name="login"),
    path('doctor-login/',views.dlogin,name="doctor-login"),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.register,name="register"),
    # appoinments
    path('appoinments/',views.appoinments,name="appoinments"),
    path('book-appoinments/',views.bookappoinments,name="book-appoinments"),
]
