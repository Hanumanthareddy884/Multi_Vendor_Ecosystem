from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Order, OrderItem

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
            is_paid=True # We will set this to False later when we add real payments
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