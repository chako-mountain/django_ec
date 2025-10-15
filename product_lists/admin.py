from django.contrib import admin
# from .models import ProductList
from .models import ProductList, CartList, CartProduct, Order, OrderProduct

# Register your models here.

admin.site.register(ProductList)
admin.site.register(CartList)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)