from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from .views import CreateTodo, ViewTodos,UpdateTodo,DeleteTodo,DeleteTodoSuccessPage,ViewNotifications,HomePage
from django.contrib.auth import views as auth_view
from .views import *


urlpatterns = [
    path('', views.signin,name="signin"),
    path('UserDashBoard/', UserDashBoard.as_view(), name='UserDashBoard'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('CreateTodo/', CreateTodo.as_view(), name='CreateTodo'),
    path('Viewtodos/', ViewTodos.as_view(), name='ViewTodos'),
    path('UpdateTodo/<str:pk>',UpdateTodo.as_view(), name='UpdateTodo'),
    path('update_password/',auth_view.PasswordChangeView.as_view(template_name="update_password.html",success_url="home" ),name='update_password'),
    path('DeleteTodo/<str:pk>',DeleteTodo.as_view(), name='DeleteTodo'),
    path('DeleteTodoSuccessPage/', DeleteTodoSuccessPage.as_view(), name='DeleteTodoSuccessPage'),
    path('update_todo_status/<str:pk>',views.update_todo_status, name='update_todo_status'),
    path('HomePage/',HomePage.as_view(), name='HomePage'),
    
]