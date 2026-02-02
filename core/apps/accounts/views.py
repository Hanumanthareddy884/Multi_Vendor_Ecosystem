from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from store.models import Product


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user return redirect('frontpage')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        return redirect('frontend')

    # get the product belongs to this vendor
    products = request.user.products.all()

    # We will eventually add orders here too
    return render(request, 'accounts/vendor_dashboard.html',
                  { 'products': products })
