from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'image')  # Add 'image' here

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','in_stock','category','created_at')
    list_filter = ('in_stock','category')
    search_fields = ('title','description')
    prepopulated_fields = {'slug': ('title',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','email','created_at','paid')
    inlines = [OrderItemInline]
