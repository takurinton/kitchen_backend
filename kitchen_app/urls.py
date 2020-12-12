from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.OperationUser.as_view()),
    path('create/', views.CreateUser.as_view()), 
    path('cart/', views.OperationCart.as_view()), 
    path('done/', views.CartSubmit.as_view()), 
    path('items/', views.GetItems.as_view()), 
    path('item/<str:name>', views.GetItem.as_view()), 
]