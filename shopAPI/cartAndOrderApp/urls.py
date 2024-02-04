from django.urls import path
from . import views

urlpatterns = [
    path('order', views.OrderItemView.as_view()),
]