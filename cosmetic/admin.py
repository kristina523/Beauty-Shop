from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'get_total_price']  
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₽"
    get_total_price.short_description = "Общая сумма"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_cost', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['cart__user__username', 'product__name']