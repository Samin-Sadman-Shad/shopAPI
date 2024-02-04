# from django.db import models
#
#
# # Create your models here.
# class Category(models.Model):
#     title = models.CharField(max_length=255, db_index=True)
#     objects = models.Manager()
#
#
# class MenuItem(models.Model):
#     title = models.CharField(max_length=255, db_index=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
#     featured = models.BooleanField(db_index=True)
#     category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.title
