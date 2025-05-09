from rest_framework import serializers
from cosmetic.models import User, Brand, Category, Product, Order, OrderItem, Review, CartItem, ReferralProgram

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['user_id', 'password_hash']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['brand_id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['category_id']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discounted_price']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['product_id']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['order_id']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['item_id']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['review_id']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ['id']

class ReferralProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralProgram
        exclude = ['referral_id']