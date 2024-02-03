from django.shortcuts import render
from rest_framework import generics, status
from .models import MenuItem, Category
from .serializers import CategorySerializer, MenuItemSerializer


# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
