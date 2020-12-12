from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, status, viewsets, filters

from .models import User, Cart, InCartItems, Item
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
    
    def delete(self, request):
        user = request.user 
        user.delete()
        return Response({'status': 'delete ok'})

    
class OperationCart(APIView):
    def get(self, request):
        user = request.user 
        try:
            cart = Cart.objects.get(user=user, is_active=True)
            if not cart.is_active:
                return Response({'status': 'cart is not valid'})
        except:
            return Response({'status': 'cart is empty'})
        
        items = InCartItems.objects.filter(cart=cart)
        
        res = {
            'items': [
                {
                    # ここのSQL怪しいので後で確認、とりま動くものを
                    'item': item.item.name, 
                    'number': item.number
                }
                for item in items
            ], 
            'price': sum_price(items)
        }

        return Response(res)
    
    def post(self, request):
        user = request.user 
        data = request.data

        if not add_cart(user, data):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)
    
class CartSubmit(APIView):
    # TODO: メール送信の処理
    def post(self, request):
        user = request.user 
        date = request.data['date']

        try:
            cart = Cart.objects.get(user=user, is_active=True)
            if not cart.is_active:
                return Response({'status': 'cart is not valid'})
        except:
            return Response({'status': 'cart is empty'})
        
        cart.is_active = False 
        cart.date = date
        cart.save()

        return Response({'status': 'ok'})

        
class GetItems(APIView):
    def get(self, request):
        items = Item.objects.all()
        res = [
            {
                'name': item.name, 
                'expo': item.expo, 
                'price': item.price, 
            }
            for item in items
        ]

        return Response(res)


class GetItem(APIView):
    def get(self, request, name):
        item = Item.objects.get(name=name)
        res = {
            'name': item.name, 
            'expo': item.expo, 
            'price': item.price
        }

        return Response(res)


def add_cart(user, data):
    _item = data['item']
    number = int(data['number'])

    try:
        item = Item.objects.get(name=_item)
    except:
        return False

    try:
        cart = Cart.objects.get(user=user, is_active=True)
    except:
        cart = Cart(user=user, is_active=True).save()
        cart.save()

    try:
        in_cart_items = InCartItems.objects.get(cart=cart, item=item)
        in_cart_items.number += number
    except:
        in_cart_items = InCartItems(cart=cart, item=item, number=number)
        
    in_cart_items.save()

    return True

def sum_price(items):
    # 要修正
    price = [item.item.price*item.number for item in items]
    return sum(price)