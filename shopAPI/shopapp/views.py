from datetime import date
from decimal import Decimal

from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from shopapp.models import MenuItem, Category, OrderItem, Cart, Order
from shopapp.serializers import MenuItemSerializer, CategorySerializer, OrderItemSerializer, CartSerializer, \
    OrderSerializer, UserSerializer, CartMenuItemUpdateSerializer
from .filters import MenuItemFilterSet

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.db.models import Q


# Create your views here.
class MenuItemsView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['category', 'title', 'price']
    filterset_class = MenuItemFilterSet
    search_fields = ["title", "price"]
    ordering_fields = ['price', 'id']
    ordering = ["price"]
    permission_classes = []

    # def checkAdmin(self, request, code: int):
    #     if request.user.group == "Manager":
    #         return Response(status=code)
    #     else:
    #         return Response(status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        self.permission_classes = []
        # serialized_item = MenuItemSerializer(self.get_queryset(), many=True)
        serialized_item = MenuItemSerializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(
                {'success': 'true', 'message': 'new menu item created successfully', 'data': serialized_item.data},
                status=status.HTTP_201_CREATED)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            return Response({'success': 'true', 'message': 'Please use url with id to update'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            return Response({'success': 'true', 'message': 'Please use url with id to update'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            return Response({'success': 'true', 'message': 'Please use url with id to update'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = []
        pk = kwargs.get('pk')
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            pk = kwargs.get('pk')
            item = get_object_or_404(MenuItem, pk=pk)
            serialized_item = MenuItemSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(
                {'success': 'true', 'message': 'new menu item updated successfully', 'data': serialized_item.data},
                status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            pk = kwargs.get('pk')
            item = get_object_or_404(MenuItem, pk=pk)
            serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(
                {'success': 'true', 'message': 'new menu item updated successfully', 'data': serialized_item.data},
                status=status.HTTP_200_OK)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        if request.user.groups.filter(name="Manager").exists():
            pk = kwargs.get('pk')
            item = get_object_or_404(MenuItem, pk=pk)
            item.delete()
            return Response({'success': 'true', 'message': 'menu item deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'success': 'false', 'message': 'user is not authorized to perform the action'},
                            status=status.HTTP_403_FORBIDDEN)


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategorySingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.groups.filter(name="Manager").exists():
            query = OrderItem.objects.all()
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            query = OrderItem.objects.filter(delivery_crew=self.request.user)
        else:
            query = OrderItem.objects.filter(user=self.request.user)
        return query

    def create(self, request, *args, **kwargs):
        if not request.user.groups.count() == 0:
            cart_items = Cart.objects.filter(user=request.user)
            total = self.calculate_total(cart_items)
            order = Order.objects.create(user=request.user, status=False, total_price=total, date=date.today())
            # place every cart item to order item, and remove the card item
            for cart_item in cart_items.values():
                menu_item = get_object_or_404(MenuItem, id=cart_item['menu_item_id'])
                order_item = OrderItem.objects.create(order=order, menu_item=menu_item, quantity=cart_item['quantity'],
                                                      unit_price=cart_item['unit_price'],
                                                      total_price=cart_item['total_price'])
                order_item.save()
            cart_items.delete()
            return Response({'success': 'true',
                             'message': 'Your order has been placed with {} order number'.format(str(order.id))},
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        order = Order.objects.get(pk=pk)
        if request.user == order.user:
            order_items = OrderItem.objects.filter(order=kwargs['order_id'])
            serialized_item = OrderItemSerializer(order_items, many=True)
            return Response(serialized_item.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter("Manager").exists():
            pk = kwargs['pk']
            # order = Order.objects.get(pk=pk)
            order = get_object_or_404(Order, pk=pk)
            # if not order.status:
            #     order.status = True
            order.status = not order.status
            delivery_crew_pk = request.data['delivery_crew']
            delivery_crew = get_object_or_404(User, pk=delivery_crew_pk)
            order.delivery_crew = delivery_crew
            serialized_item = OrderSerializer(Order, request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user.groups.filter("Deliver crew").exists():
            pk = kwargs['pk']
            # order = Order.objects.get(pk=pk)
            order = get_object_or_404(Order, pk=pk)
            # if not order.status:
            #     order.status = True
            order.status = not order.status
            order.save()
            return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter('Manager').exists():
            pk = kwargs['pk']
            order = get_object_or_404(Order, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CartMenuItemView(generics.ListAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    # queryset = Cart.objects.all()
    serializer_class = CartMenuItemUpdateSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        items = Cart.objects.select_related("menu_item")

        return items
        # user = self.request.user
        # return Cart.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        menu_items_data = [{'menu_item': item['menu_item']} for item in serializer.data]

        return Response(menu_items_data)

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

    def partial_update(self, request, *args, **kwargs):
        request_data = {k: v for k, v in request.data.items() if k == 'menu_item_id'}
        kwargs['partial'] = True
        kwargs['data'] = request_data

        return super().partial_update(request, *args, **kwargs)

    # def get_serializer_class(self, *args, **kwargs):
    #     fields = ['menu_item_id']
    #     if self.request.method == 'PATCH' and 'data' in kwargs:
    #         data = kwargs['data']
    #         data = {k: v for k, v in data.items() if k in fields}
    #         kwargs['data'] = data
    #     return super().get_serializer(*args, **kwargs)


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ManagerView(generics.ListCreateAPIView):
    pass


class ManagerRemoveUserView(generics.DestroyAPIView):
    pass
