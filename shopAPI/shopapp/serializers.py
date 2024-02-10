from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, MenuItem, Order, OrderItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ['id']
        fields = ['id', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'id']


class CartSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.IntegerField(write_only=True)
    menu_item = MenuItemSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'user', 'menu_item_id', 'menu_item', 'quantity', 'unit_price', 'total_price']


class CartMenuItemUpdateSerializer(CartSerializer):
    class Meta(CartSerializer.Meta):
        model = Cart
        extra_kwargs: {
            'user_id': {'read_only': True},
            'user': {'read_only': True},
            'menu_item': {'read_only': True},
            'quantity': {'read_only': True},
            'unit_price': {'read_only': True},
            'total_price': {'read_only': True}
        }


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menu_item_id', 'menu_item', 'quantity']
        extra_kwargs = {
            'menu_item': {'read_only': True},
        }


class RemoveCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menu_item_id', 'menu_item']
        extra_kwargs = {
            'menu_item': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'user', 'delivery_crew', 'status', 'total_price', 'date', 'user_id',
                  'delivery_crew_id']


class ManagerOrderSerializer(serializers.ModelSerializer):
    delivery_crew_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = ['delivery_crew_id', 'delivery_crew', 'status']
        # A manager can set a delivery crew to this order,
        # and update the order status to 0 or 1


class CrewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        # The delivery crew will not be able to update anything else in this order.


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrderSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'order', 'menu_item_id', 'menu_item', 'quantity', 'unit_price', 'total_price']
