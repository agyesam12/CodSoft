from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('about/',views.about, name='about'),
    path('signout/',views.signout, name='signout'),
]