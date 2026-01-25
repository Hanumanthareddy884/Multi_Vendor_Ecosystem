from django.shortcuts import render, redirect
from .cart import Cart


# Create your views here.
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('frontend')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')

