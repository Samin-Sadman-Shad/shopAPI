# from django.db import models
# from MenuItemApp.models import Category, MenuItem
# from django.contrib.auth.models import User
#
#
# # Create your models here.
# class Cart(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     menu_item = models.ForeignKey(to=MenuItem, on_delete=models.CASCADE)
#     quantity = models.SmallIntegerField()
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)
#     total_price = models.DecimalField(max_digits=6, decimal_places=2)
#     objects = models.Manager()
#
#     class Meta:
#         unique_together = ['menu_item', 'user']
#
#
# class Order(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     delivery_crew = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
#     status = models.BooleanField(db_index=True)
#     total_price = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField(db_index=True)
#     objects = models.Manager()
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
#     menu_item = models.ForeignKey(to=MenuItem, on_delete=models.CASCADE)
#     quantity = models.SmallIntegerField()
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)
#     total_price = models.DecimalField(max_digits=6, decimal_places=2)
#     objects = models.Manager()
#
#     class Meta:
#         unique_together = ['order', 'menu_item']