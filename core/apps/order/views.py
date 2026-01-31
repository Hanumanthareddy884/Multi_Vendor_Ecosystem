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

    return render(request, 'order/checkout.html', {'cart': cart})


def create_checkout_session(request):
    cart: Cart(request)
    stripe.api_key = settings.apSTRIPE_SECRET_KEY

    # prepare the line items for stripe
    items = []
    for item in cart:
        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['product'].title},
                'unit_amount': int(item['product'].price * 100),  # Stripe uses a cents
            },
            'quantity': item['quantity'],
        })

        # Create stripe session
        session = stripe.checkout.Session.create(
            ayment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/success/',
            cancel_url='http://127.0.0.1:8000/cart/',
        )
        return JsonResponse({'sessionId': session.id})

def success_view(request):
    return render(request,'success')