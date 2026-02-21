from django.contrib import admin
from .models import Post, Order

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'post', 'delivery_date', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'delivery_date', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
