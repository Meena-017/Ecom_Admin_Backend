from django.contrib import admin
from website.models import Products
from website.models import ProductImage
from website.models import AuthUser
# Register your models here.
admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(AuthUser)