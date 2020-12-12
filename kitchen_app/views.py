from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User

class GetUser(APIView):
    def get(self, request):
        user = request.user
        res = {
            'email': user.email, 
            'is_staff': user.is_staff, 
            'is_active': user.is_active, 
        }
        
        return Response(res)