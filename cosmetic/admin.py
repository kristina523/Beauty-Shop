from django.contrib import admin
from .models import User, Brand, Category, Product, Order, OrderItem, Review, CartItem, ReferralProgram

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'bonus_points', 'personal_discount')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'parent')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'category', 'brand', 'stock_quantity', 'is_best_seller')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'order_date', 'total_amount', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'quantity', 'price_at_purchase')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'product', 'user', 'rating', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')

@admin.register(ReferralProgram)
class ReferralProgramAdmin(admin.ModelAdmin):
    list_display = ('referral_id', 'referrer', 'referred', 'referral_date', 'is_used')