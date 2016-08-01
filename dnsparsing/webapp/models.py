from __future__ import unicode_literals

from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length = 100)
    hreference = models.CharField(max_length = 400)
    product_price = models.FloatField()
    def __str__(self):
        return '%s' % (self.product_name)
