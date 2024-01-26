from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Vendor


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    preview = models.ImageField(upload_to='previews', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', _('В наличии')),
        ('out_of_stock', _('Нет в наличии'))
    )

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    specifications = RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preview = models.ImageField(upload_to='previews', blank=True, null=True)
    discount = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_stock')
    category = models.ManyToManyField(Category, blank=True, related_name='products')
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, related_name='products', null=True, on_delete=models.SET_NULL)
