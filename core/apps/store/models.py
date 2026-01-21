from django.db import models
from django.conf import  settings # To link Product to a Vendor

# Create your models here.
# store_category
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # For SEO friendly URLs (e.g., /store/shoes/)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
# store_product
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Use Decimal for money!
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnails/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',) # Show newest products first

    def __str__(self):
        return self.title