from django.shortcuts import render
from rest_framework import generics

from shopapp.models import MenuItem, Category, OrderItem, Cart, Order
from shopapp.serializers import MenuItemSerializer, CategorySerializer, OrderItemSerializer, CartSerializer, OrderSerializer, UserSerializer
from .filters import MenuItemFilterSet

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # filter this endpoint with following fields
    # filterset_fields = ['category', 'title', 'price']
    filterset_class = MenuItemFilterSet
    # search_fields = ["title", "price"]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CartMenuItemView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        items = Cart.objects.values("menu_item")
        return items

    # def perform_update(self, serializer):
    #     instance = self.get_object()
    #     self.request.data.get("menu-item")
