import json

from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Order, OrderItem
import stripe
from django.conf import settings
from django.http import JsonResponse


def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        # Create the order object with form data
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            zipcode=request.POST.get('zipcode'),
            place=request.POST.get('place'),
            paid_amount=cart.get_total_cost(),
            is_paid=True  # We will set this to False later when we add real payments
        )

        # Move items from Cart to OrderItem table
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Clear the session cart
        cart.clear()

        return render(request, 'order/success.html')

    return render(request, 'order/checkout.html', {'cart': cart, 'pub_key': settings.STRIPE_PUB_KEY})


def create_checkout_session(request):
    cart = Cart(request)
    # Load the JSON data from the JavaScript fetch
    data = json.loads(request.body)

    # 1. Create the Order in our database (Status: Unpaid)
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        address=data.get('address'),
        zipcode=data.get('zipcode'),
        place=data.get('place'),
        paid_amount=cart.get_total_cost(),
        is_paid=False  # This stays False until Stripe confirms
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )

    # 2. Tell Stripe about the items
    stripe.api_key = settings.STRIPE_SECRET_KEY
    items = []
    for item in cart:
        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['product'].title},
                'unit_amount': int(item['product'].price * 100),
            },
            'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        # Pass the order ID to Stripe so we can find it later
        client_reference_id=order.id,
        success_url='http://127.0.0.1:8000/order/success/',
        cancel_url='http://127.0.0.1:8000/cart/',
    )

    return JsonResponse({'id': session.id})


def success_view(request):
    print("Reddy",request)
    return render(request, 'order/success.html')
