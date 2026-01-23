from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # This automatically fills the slug (user friendly text) based title
    prepopulated_fileds = {'slug':('title',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'price', 'date_added']
    list_filter = ['category', 'date_added']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}