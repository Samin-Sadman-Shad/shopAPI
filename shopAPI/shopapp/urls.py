from django.urls import path
from . import views

urlpatterns = [
    path('order', views.OrderItemView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
]