from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.

def frontend(request):
    # Fetch the 8 most recent products
    products = Product.objects.all()[0:8]
    category = Category.objects.all()
    return render(request, 'store/frontend.html', {
        'products': products,
        'category': category
    })


def product_detail(request, category_slug, slug):
    # This fetches the product using the slug from the URL
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'store/product_detail.html', {
        'product': product
    })
def category_detail(request, slug=None):
    # get_object_or_404(model,id=1 or title = "sfsdf" or slug) here we are using slug for SEO
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    print(category, products)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })
