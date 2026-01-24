from django.shortcuts import render
from .models import Product
# Create your views here.

def frontend(request):
    # Fetch the 8 most recent products
    products = Product.objects.all()[0:8]

    return render(request,'store/frontend.html',{
                      'products':products
                  })

