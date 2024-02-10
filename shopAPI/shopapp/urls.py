from django.urls import path
from . import views

urlpatterns = [
    path('order', views.OrdersView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('category/<int:pk>python ', views.CategorySingleView.as_view()),
    path('cart/menu-items', views.CartMenuItemView.as_view()),
    path('cart', views.CartView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('groups/manager/users', views.ManagerGroupUserView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerGroupSingleUserView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewGroupView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewGroupSingleView.as_view()),
]