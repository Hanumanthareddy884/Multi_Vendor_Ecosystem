from django.conf import settings
from store.models import Product
from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(Product.objects.get(pk=product_id).price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products: cart[str(product.id)]['product'] = product
        for item in cart.values(): item['price'] = Decimal(item['price'])
        item['total_price'] = item['price'] * item['quantity']
        yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}