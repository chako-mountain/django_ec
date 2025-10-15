# from django.db import IntegrityError
# from django.shortcuts import render, redirect
# from product_lists.models import ProductList, CartList, CartProduct,Order,OrderProduct
# from django.http import HttpResponseRedirect 
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.core.exceptions import ValidationError
# # from basicauth.decorators import basic_auth_required
# from django.shortcuts import get_object_or_404
# import uuid
# from django.db.models import Sum
# from django.contrib import messages


# def product_list_view(request):
#     session_key = request.session.setdefault('key', str(uuid.uuid4()))
#     obj, _ = CartList.objects.get_or_create(session_key=session_key)
#     try:
#         item_sum = obj.total_item_count()
#     except CartProduct.DoesNotExist:
#         redirect("lists")
#     product = ProductList.objects.all()
#     return render(request, 'lists.html', {'object_list': product, "item_sum":item_sum})


# def product_detail_view(request, id,):
#     session_key = request.session.get('key', None)
#     try:
#         cart = CartList.objects.get(session_key=session_key)
#         item_sum = cart.total_item_count()
#     except CartProduct.DoesNotExist:
#         redirect("lists")
#     related_product = ProductList.objects.order_by("-created_at")[:4]
#     product = get_object_or_404(ProductList, id=id)
#     return render(request, 'details.html', {"related_products": related_product, "product": product, "item_sum":item_sum})


# # @basic_auth_required
# def admin_product_list_view(request):
#     products = ProductList.objects.all()
#     return render(request, 'administrator.html', {'object_list': products})



# # @basic_auth_required
# def product_create_view(request):
#     if request.method == "POST":
#         product = ProductList()
#         product.name = request.POST.get("name", "").strip()
#         product.description = request.POST.get("description", "").strip()
#         product.is_sale = request.POST.get("is_sale") == "on"
#         product.img = request.POST["img"]
#         product.price = request.POST["price"]
#         product.star_rating = request.POST["rating"]
#         try:
#             price = int(product.price) if product.price else None
#             star_rating = int(product.star_rating) if product.star_rating else None 
#             product.price = price
#             product.star_rating = star_rating
#             product.save()
#             return redirect("administrator")    
#         except (ValidationError, ValueError):
#             error_message = "PriceまたはStar Ratingは整数で記入してね"
#             return render(request, "administrator.html" ,{ "product_list" : product, "error_message":error_message })
#     return redirect('administrator')


# # @basic_auth_required
# def product_delete_view(request):
#     delete_id = request.POST["post_id"]
#     ProductList.objects.filter(id = delete_id).delete()
#     return redirect('administrator')


# # @basic_auth_required
# def product_edit_view(request, id):
#     product = ProductList.objects.get(id=id)
#     return render(request, "edit.html" ,{ "edit_list" : product })


# # @basic_auth_required
# def product_update_view(request ,id):
#     product = ProductList.objects.get(id=id)
#     product.name = request.POST.get("name", "").strip()
#     product.description = request.POST.get("description", "").strip()
#     product.is_sale = request.POST.get("is_sale") == "on"
#     product.img = request.POST["img"]
#     price_str = request.POST.get("price", "").strip()     # POSTデータを直接取得
#     rating_str = request.POST.get("rating", "").strip()
#     try: 
#         price = int(price_str) if price_str else None
#         star_rating = int(rating_str) if rating_str else None
#         product.price = price
#         product.star_rating = star_rating
#         product.save()
#         return redirect("administrator") 
#     except (ValidationError, ValueError):
#         error_message = "PriceまたはStar Ratingは整数で記入してね"
#         product.price = price_str
#         product.star_rating = rating_str
#         return render(request, "edit.html", { "edit_list": product, "error_message": error_message })


# # @basic_auth_required
# def admin_page(request):
#     return redirect("administrator")


# def add_products_view(request):
#     if request.method == "POST":
#         session_key = request.session.get('key', 'none')
#         cart = CartList.objects.get(session_key=session_key)
#         product_id = request.POST.get("id")  # formから送信されたproductのID
#         product = ProductList.objects.get(id=product_id)
#         source = request.POST.get("source")
#         add_number = int(request.POST.get("number", 1)) if source == "from_details" else 1
#         cart_product, created = CartProduct.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={'number': add_number},
#         )
#         if not created:
#             cart_product.number += add_number
#             cart_product.save()
#     return redirect("lists")


# def cart_view(request):
#     session_key = request.session.get('key', 'none')
#     try:
#         cart_products = CartList.objects.get(session_key=session_key).cart_products.all()
#         cart = CartList.objects.get(session_key=session_key)
#         total_price = cart.total_price()
#         total_goods = cart.total_quantity()
#         return render(request, "carts.html", {"carts": cart_products, "total_price": total_price, "total_number": total_goods})
#     except CartList.DoesNotExist:
#         print("ユーザーが見つかりませんでした")
#         return render(request, "carts.html", {"carts": []})


# def cart_delete_view(request):
#     id = request.POST.get("delete")
#     cart_product = CartProduct.objects.get(id=id)
#     cart_product.delete()
    
#     session_key = str(request.session.get('key', None))
#     user = CartList.objects.get(session_key=session_key)
#     if Order.objects.filter(cart=user.id).exists():
#         return redirect("is-saved")
#     return redirect("cart")


# def cart_checkout_view(request):
#     session_key = str(request.session.get('key', None))
#     obj = CartList.objects.get(session_key=session_key)
#     cart_products = CartProduct.objects.filter(cart=obj.id)

#     user = CartList.objects.get(session_key=session_key)
#     if Order.objects.filter(cart=user.id).exists():
#         order = Order.objects.get(cart=user.id)
#         for cart_product in cart_products:
#             order_products = OrderProduct()
#             order_products.order = order
#             order_products.product_name = cart_product.product.name
#             order_products.product_price = cart_product.product.price
#             order_products.quantity = cart_product.number
#             order_products.save()

#     else:
#         order = Order()
#         billing_details = request.POST
#         order.cart = obj
#         order.first_name = billing_details.get("first_name")
#         order.last_name = billing_details.get("last_name")
#         order.user_name = billing_details.get("user_name")
#         order.email = billing_details.get("email")
#         order.address = billing_details.get("address1")
#         order.address2 = billing_details.get("address2")
#         order.country = billing_details.get("country")
#         order.state = billing_details.get("state")
#         order.zip = billing_details.get("zip")
#         order.name_on_card = billing_details.get("name_on_card")
#         order.credit_card_number = billing_details.get("card_number")
#         order.expiry_date = billing_details.get("expiration")
#         order.CVV = billing_details.get("CVV")
#         order.save()

#         for cart_product in cart_products:
#             order_products = OrderProduct()
#             order_products.order = order
#             order_products.product_name = cart_product.product.name
#             order_products.product_price = cart_product.product.price
#             order_products.quantity = cart_product.number
#             order_products.save()
#     cart_products.delete()

#     messages.success(request, "ご購入ありがとうございました！注文が正常に完了しました。")
#     return redirect("lists")


# def is_credit_card_saved(request):
#     session_key = str(request.session.get('key', None))
#     user = CartList.objects.get(session_key=session_key)
#     if Order.objects.filter(cart=user.id).exists():
#         try:
#             previous_credit_card_data = Order.objects.get(cart=user.id)
#             cart_products = CartList.objects.get(session_key=session_key).cart_products.all()
#             cart = CartList.objects.get(session_key=session_key)
#             total_price = cart.total_price()
#             total_goods = cart.total_quantity()
#             return render(request,"cart_only.html", {"previous_credit_card_data": previous_credit_card_data,"carts": cart_products, "total_price": total_price, "total_number": total_goods})
#         except CartList.DoesNotExist:
#             print("ユーザーが見つかりませんでした")
#             return render(request, "carts.html", {"carts": []})
#     else:
#         return redirect("cart")
    
        
        
# def bought_list_view(request):
#     session_key = str(request.session.get('key', None))
#     user = CartList.objects.get(session_key=session_key)
#     order = Order.objects.get(cart=user.id)
#     bought_list = OrderProduct.objects.filter(order=order.id)
#     return render(request, "bought_list.html" ,{"bought_list":bought_list, "order_info":order})




from django.db import IntegrityError
from django.shortcuts import render, redirect
from product_lists.models import ProductList, CartList, CartProduct,Order,OrderProduct
from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
# from basicauth.decorators import basic_auth_required
from django.shortcuts import get_object_or_404
import uuid
from django.db.models import Sum
from django.contrib import messages
import os
import requests


def product_list_view(request):
    session_key = request.session.setdefault('key', str(uuid.uuid4()))
    obj, _ = CartList.objects.get_or_create(session_key=session_key)
    try:
        item_sum = obj.total_item_count()
    except CartProduct.DoesNotExist:
        redirect("lists")
    product = ProductList.objects.all()
    send_simple_message()
    
    return render(request, 'lists.html', {'object_list': product, "item_sum":item_sum})


def product_detail_view(request, id,):
    session_key = request.session.get('key', None)
    try:
        cart = CartList.objects.get(session_key=session_key)
        item_sum = cart.total_item_count()
    except CartProduct.DoesNotExist:
        redirect("lists")
    related_product = ProductList.objects.order_by("-created_at")[:4]
    product = get_object_or_404(ProductList, id=id)
    return render(request, 'details.html', {"related_products": related_product, "product": product, "item_sum":item_sum})


# @basic_auth_required
def admin_product_list_view(request):
    products = ProductList.objects.all()
    return render(request, 'administrator.html', {'object_list': products})



# @basic_auth_required
def product_create_view(request):
    if request.method == "POST":
        product = ProductList()
        product.name = request.POST.get("name", "").strip()
        product.description = request.POST.get("description", "").strip()
        product.is_sale = request.POST.get("is_sale") == "on"
        product.img = request.POST["img"]
        product.price = request.POST["price"]
        product.star_rating = request.POST["rating"]
        try:
            price = int(product.price) if product.price else None
            star_rating = int(product.star_rating) if product.star_rating else None 
            product.price = price
            product.star_rating = star_rating
            product.save()
            return redirect("administrator")    
        except (ValidationError, ValueError):
            error_message = "PriceまたはStar Ratingは整数で記入してね"
            return render(request, "administrator.html" ,{ "product_list" : product, "error_message":error_message })
    return redirect('administrator')


# @basic_auth_required
def product_delete_view(request):
    delete_id = request.POST["post_id"]
    ProductList.objects.filter(id = delete_id).delete()
    return redirect('administrator')


# @basic_auth_required
def product_edit_view(request, id):
    product = ProductList.objects.get(id=id)
    return render(request, "edit.html" ,{ "edit_list" : product })


# @basic_auth_required
def product_update_view(request ,id):
    product = ProductList.objects.get(id=id)
    product.name = request.POST.get("name", "").strip()
    product.description = request.POST.get("description", "").strip()
    product.is_sale = request.POST.get("is_sale") == "on"
    product.img = request.POST["img"]
    price_str = request.POST.get("price", "").strip()     # POSTデータを直接取得
    rating_str = request.POST.get("rating", "").strip()
    try: 
        price = int(price_str) if price_str else None
        star_rating = int(rating_str) if rating_str else None
        product.price = price
        product.star_rating = star_rating
        product.save()
        return redirect("administrator") 
    except (ValidationError, ValueError):
        error_message = "PriceまたはStar Ratingは整数で記入してね"
        product.price = price_str
        product.star_rating = rating_str
        return render(request, "edit.html", { "edit_list": product, "error_message": error_message })


# @basic_auth_required
def admin_page(request):
    return redirect("administrator")


def add_products_view(request):
    if request.method == "POST":
        session_key = request.session.get('key', 'none')
        cart = CartList.objects.get(session_key=session_key)
        product_id = request.POST.get("id")  # formから送信されたproductのID
        product = ProductList.objects.get(id=product_id)
        source = request.POST.get("source")
        add_number = int(request.POST.get("number", 1)) if source == "from_details" else 1
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'number': add_number},
        )
        if not created:
            cart_product.number += add_number
            cart_product.save()
    return redirect("lists")


def cart_view(request):
    session_key = request.session.get('key', 'none')
    try:
        cart_products = CartList.objects.get(session_key=session_key).cart_products.all()
        cart = CartList.objects.get(session_key=session_key)
        total_price = cart.total_price()
        total_goods = cart.total_quantity()
        return render(request, "carts.html", {"carts": cart_products, "total_price": total_price, "total_number": total_goods})
    except CartList.DoesNotExist:
        print("ユーザーが見つかりませんでした")
        return render(request, "carts.html", {"carts": []})


def cart_delete_view(request):
    id = request.POST.get("delete")
    cart_product = CartProduct.objects.get(id=id)
    cart_product.delete()
    
    session_key = str(request.session.get('key', None))
    user = CartList.objects.get(session_key=session_key)
    if Order.objects.filter(cart=user.id).exists():
        return redirect("is-saved")
    return redirect("cart")


def cart_checkout_view(request):
    session_key = str(request.session.get('key', None))
    obj = CartList.objects.get(session_key=session_key)
    cart_products = CartProduct.objects.filter(cart=obj.id)

    user = CartList.objects.get(session_key=session_key)
    if Order.objects.filter(cart=user.id).exists():
        order = Order.objects.get(cart=user.id)
        for cart_product in cart_products:
            order_products = OrderProduct()
            order_products.order = order
            order_products.product_name = cart_product.product.name
            order_products.product_price = cart_product.product.price
            order_products.quantity = cart_product.number
            order_products.save()

    else:
        order = Order()
        billing_details = request.POST
        order.cart = obj
        order.first_name = billing_details.get("first_name")
        order.last_name = billing_details.get("last_name")
        order.user_name = billing_details.get("user_name")
        order.email = billing_details.get("email")
        order.address = billing_details.get("address1")
        order.address2 = billing_details.get("address2")
        order.country = billing_details.get("country")
        order.state = billing_details.get("state")
        order.zip = billing_details.get("zip")
        order.name_on_card = billing_details.get("name_on_card")
        order.credit_card_number = billing_details.get("card_number")
        order.expiry_date = billing_details.get("expiration")
        order.CVV = billing_details.get("CVV")
        order.save()

        for cart_product in cart_products:
            order_products = OrderProduct()
            order_products.order = order
            order_products.product_name = cart_product.product.name
            order_products.product_price = cart_product.product.price
            order_products.quantity = cart_product.number
            order_products.save()
    cart_products.delete()

    messages.success(request, "ご購入ありがとうございました！注文が正常に完了しました。")
    return redirect("lists")


def is_credit_card_saved(request):
    session_key = str(request.session.get('key', None))
    user = CartList.objects.get(session_key=session_key)
    if Order.objects.filter(cart=user.id).exists():
        try:
            previous_credit_card_data = Order.objects.get(cart=user.id)
            cart_products = CartList.objects.get(session_key=session_key).cart_products.all()
            cart = CartList.objects.get(session_key=session_key)
            total_price = cart.total_price()
            total_goods = cart.total_quantity()
            return render(request,"cart_only.html", {"previous_credit_card_data": previous_credit_card_data,"carts": cart_products, "total_price": total_price, "total_number": total_goods})
        except CartList.DoesNotExist:
            print("ユーザーが見つかりませんでした")
            return render(request, "carts.html", {"carts": []})
    else:
        return redirect("cart")
    
        
def bought_list_view(request):
    session_key = str(request.session.get('key', None))
    user = CartList.objects.get(session_key=session_key)
    order = Order.objects.get(cart=user.id)
    bought_list = OrderProduct.objects.filter(order=order.id)
    return render(request, "bought_list.html" ,{"bought_list":bought_list, "order_info":order})


# def send_simple_message():
#   	return requests.post(
#   		"https://api.mailgun.net/v3/sandboxde043ff338654f72a5c5ba39d98c2272.mailgun.org/messages",
#   		auth=("api", os.getenv('API_KEY', 'API_KEY')),
#   		data={"from": "Mailgun Sandbox <postmaster@sandboxde043ff338654f72a5c5ba39d98c2272.mailgun.org>",
# 			"to": "taiga <gonzaburouduanyewufu@gmail.com>",
#   			"subject": "Hello taiga",
#   			"text": "Congratulations taiga, you just sent an email with Mailgun! You are truly awesome!"})


def send_simple_message():
    response = requests.post(
        f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={
            "from": f"Mailgun Sandbox <postmaster@{os.getenv('MAILGUN_DOMAIN')}>",
            "to": "taiga <gonzaburouduanyewufu@gmail.com>",
            "subject": "Hello taiga",
            "text": "Congratulations taiga, you just sent an email with Mailgun! You are truly awesome!"
        }
    )
    print("Mailgun Response:", response.status_code, response.text)  # ここで確認
    return response
