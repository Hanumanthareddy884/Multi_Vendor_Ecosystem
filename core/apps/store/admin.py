from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # This automatically fills the slug (user friendly text) based title
    prepopulated_fileds = {'slug':('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','vendor','price','date_added')
    list_filter  = ('category','date_added')
    prepopulated_fields = {'slug',('title',)}