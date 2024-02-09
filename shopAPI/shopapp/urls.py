from django.urls import path
from . import views

urlpatterns = [
    path('order', views.OrderItemView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('category/<int:pk>', views.CategorySingleView.as_view()),
    path('cart/menu-items', views.CartMenuItemView.as_view()),
    path('cart', views.CartView.as_view()),
]