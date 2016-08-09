from __future__ import unicode_literals

from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=100)
    city_id = models.CharField(max_length=100)
    check = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.city_name

    def __unicode__(self):
        return u'%s' % self.city_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_reference = models.URLField(max_length=400)
    check = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.category_name)

    def __unicode__(self):
        return u'%s' % self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    hreference = models.URLField(max_length=400)
    product_price = models.FloatField(default=0)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.product_name)

    def __unicode__(self):
        return u'%s' % self.product_name