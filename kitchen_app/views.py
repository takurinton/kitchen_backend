from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, status, viewsets, filters

from .models import User
from .serializer import CreateUserSerializer

class CreateUser(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OperationUser(APIView):
    def get(self, request):
        user = request.user
        res = {
            'email': user.email, 
            'address': user.address, 
            'is_staff': user.is_staff, 
            'is_active': user.is_active, 
        }
        return Response(res)
    
    def put(self, request):
        user = request.user
        try:
            email = request.data['email']
        except:
            email = ''
        try:
            password = request.data['password']
        except:
            password = ''
        try:
            address = request.data['address']
        except:
            address = ''
        
        if email != '':
            user.email = email
        if password != '':
            user.password = password
        if address != '':
            user.address = address

        user.save()

        res = {
            'email': user.email, 
            'address': user.address, 
            'is_staff': user.is_staff, 
            'is_active': user.is_active, 
        }

        return Response(res)