from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, BrandViewSet, CategoryViewSet, ProductViewSet,
    OrderViewSet, OrderItemViewSet, ReviewViewSet, CartItemViewSet, ReferralProgramViewSet
)
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'cart', CartItemViewSet)
router.register(r'referrals', ReferralProgramViewSet)

urlpatterns = [
    path('', include(router.urls)),
]