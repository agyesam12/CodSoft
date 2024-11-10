from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('about/',views.about, name='about'),
    path('signout/',views.signout, name='signout'),
    path('CreateContact/',CreateContact.as_view(), name='CreateContact'),
    path('ViewContacts/',ViewContacts.as_view(), name='ViewContacts'),
    path('DeleteContact/<str:pk>',DeleteContact.as_view(), name='DeleteContact'),
    path('DeleteContactSuccessPage/', DeleteContactSuccessPage.as_view(), name='DeleteContactSuccessPage'),
    path('UpdateContact/<str:pk>',UpdateContact.as_view(), name='UpdateContact'),
    path('ContactDetailPage/<str:pk>',ContactDetailPage.as_view(), name='ContactDetailPage'),
    path('update_password/',auth_view.PasswordChangeView.as_view(template_name="update_password.html",success_url="home" ),name='update_password'),
    path('UserDashBoard/', UserDashBoard.as_view(), name='UserDashBoard'),
    path('ViewNotifications/', ViewNotifications.as_view(), name='ViewNotifications'),
    path('SendFeedBack/', SendFeedBack.as_view(), name='SendFeedBack'),
    path('AskQuestion/', AskQuestion.as_view(), name='AskQuestion'),
]