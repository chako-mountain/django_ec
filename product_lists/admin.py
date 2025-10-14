from django.contrib import admin
# from .models import ProductList
from .models import ProductList, CartList, CartProduct

# Register your models here.

admin.site.register(ProductList)
admin.site.register(CartList)
admin.site.register(CartProduct)