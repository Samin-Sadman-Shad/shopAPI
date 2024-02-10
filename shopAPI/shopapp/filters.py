from django_filters import rest_framework as filters
from .models import MenuItem


class MenuItemFilterSet(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = MenuItem
        fields = ['price', 'category', 'title']


class OrderFilterSet(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    min_date = filters.NumberFilter(field_name='date', lookup_expr='gte')
    max_date = filters.NumberFilter(field_name='date', lookup_expr='lte')