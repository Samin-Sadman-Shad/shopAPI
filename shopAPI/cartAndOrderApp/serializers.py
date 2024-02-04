# from rest_framework import serializers
# from .models import Cart, Order, OrderItem
# from MenuItemApp.serializers import MenuItemSerializer, CategorySerializer
# from django.contrib.auth.models import User
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'id']
#
#
# class CartSerializer(serializers.ModelSerializer):
#     menu_item_id = serializers.IntegerField(write_only=True)
#     menu_item = MenuItemSerializer(read_only=True)
#     user_id = serializers.IntegerField(write_only=True)
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'menu_item_id', 'menu-item', 'quantity', 'unit_price', 'total_price']
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(write_only=True)
#     user = UserSerializer(read_only=True, source='user')
#     delivery_crew_id = serializers.IntegerField(write_only=True)
#     delivery_crew = UserSerializer(read_only=True, source='delivery_crew', allow_null=True)
#
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'delivery_crew', 'status', 'total_price', 'date', 'user_id', 'delivery_crew_id']
#
#
# class OrderItemSerializer(serializers.ModelSerializer):
#     order_id = serializers.IntegerField(write_only=True)
#     order = OrderSerializer(read_only=True)
#     menu_item_id = serializers.IntegerField(write_only=True)
#     menu_item = MenuItemSerializer(read_only=True)
#
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'order_id', 'order', 'menu_item_id', 'menu_item', 'quantity', 'unit_price', 'total_price']
