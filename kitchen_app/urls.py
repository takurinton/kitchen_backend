from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.GetUser.as_view()),
]