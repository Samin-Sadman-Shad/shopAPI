from django.shortcuts import render
from rest_framework import generics, status
from .models import MenuItem, Category

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()