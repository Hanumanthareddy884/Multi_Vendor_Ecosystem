"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store.views import frontend, category_detail, product_detail
from cart.views import add_to_cart, cart_detail, remove_from_cart
from django.contrib.auth import views as auth_views  # Import Django's auth views
from accounts.views import signup,vendor_dashboard
from order.views import checkout,success_view,create_checkout_session

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontend, name='frontend'),
    path('/product/<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('api/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('order/success/', success_view, name='success'),
path('vendor-dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('<slug:slug>/', category_detail, name='category_detail'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
