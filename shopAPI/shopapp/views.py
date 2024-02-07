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
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        items = Cart.objects.values("menu_item")
        return items
        # user = self.request.user
        # return Cart.objects.filter(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()
        menu_item_id = self.request.data.get("menu_item_id")
        menu_item = MenuItem.objects.get(id=menu_item_id)
        quantity = self.request.data.get("quantity", 1)
        unit_price = menu_item.price

        other_cart_items = Cart.objects.filter(user=user).exclude(id=serializer.instance.id)
        total_price = sum(item.total_price for item in other_cart_items) + unit_price * quantity

        cart_data = {
            'user': user.id,
            'menu_item': menu_item_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
        }

        serializer.save(**cart_data)


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer