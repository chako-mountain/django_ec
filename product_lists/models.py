import uuid
from django.db import models
from django.db.models import Sum

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    
class CartList(BaseModel):
    session_key = models.UUIDField(default=uuid.uuid4(),editable=False,unique=True,)

    def __str__(self):
        return str(self.session_key)
    
    def total_price(self):
        return sum(item.product.price * item.number for item in self.cart_products.all())

    def total_quantity(self):
        return sum(item.number for item in self.cart_products.all())
    
    def total_item_count(self):
        return self.cart_products.aggregate(total=Sum('number'))['total'] or 0


class ProductList(BaseModel):
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    star_rating = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=False, null=False)
    is_sale = models.BooleanField(default=False)
    img = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    

class CartProduct(BaseModel):
    cart = models.ForeignKey(CartList, on_delete=models.PROTECT, related_name="cart_products")
    product = models.ForeignKey(ProductList, on_delete=models.PROTECT)
    number = models.IntegerField(null = False, blank = False)

    def __str__(self):
        return str(self.cart)
    

class Order(BaseModel):
    cart = models.ForeignKey(CartList, on_delete=models.PROTECT, related_name="order")
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    user_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    address2 = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    zip = models.CharField(max_length=255, null=False)

    name_on_card = models.CharField(max_length=255, null=False)
    credit_card_number = models.CharField(max_length=255, null=False)
    expiry_date = models.CharField(max_length=255, null=False)
    CVV = models.CharField(max_length=255, null=False)

    def __str__(self):
        return str(self.cart)


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="order_products")
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order)

