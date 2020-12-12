from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.OperationUser.as_view()),
    path('create/', views.CreateUser.as_view()), 
    path('cart/', views.OperationCart.as_view()), 
]