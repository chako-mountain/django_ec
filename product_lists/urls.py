
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import include
from .views import product_list_view, product_detail_view, product_create_view , product_delete_view, product_edit_view, product_update_view,admin_page,admin_product_list_view,add_products_view, cart_view, cart_delete_view, cart_checkout_view

urlpatterns = [
    path('lists' , product_list_view, name='lists' ),
    path('details' , product_detail_view, name='details' ),
    path('administrator/products', admin_product_list_view, name='administrator'),
    path('detail/<int:id>/', product_detail_view, name='detail'),
    path('administrator/products/create', product_create_view, name = "contents_add"),
    path('administrator/products/delete', product_delete_view , name = 'delete' ),
    path('administrator/products/<int:id>/edit', product_edit_view , name = 'edit' ),
    path('administrator/products/<int:id>/update', product_update_view , name = 'update' ),
    path("admin-basic/", admin_page, name="admin_page"),
    path("cart/products/add", add_products_view, name = "addproducts"),
    path("cart", cart_view, name = "cart"),
    path("cart/products/delete", cart_delete_view, name = "cart_delete"),
    path("cart_checkout", cart_checkout_view, name = "cart_checkout"),

]
