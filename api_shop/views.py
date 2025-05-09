from rest_framework import viewsets, permissions, filters
from .permissions import IsOwnerOrAdminOrReadOnly
from rest_framework import mixins, viewsets
from .pagination import NumberedPagePagination
from cosmetic.models import User, Brand, Category, Product, Order, OrderItem, Review, CartItem, ReferralProgram
from .serializers import (
    UserSerializer, BrandSerializer, CategorySerializer,
    ProductListSerializer, ProductDetailSerializer,
    OrderSerializer, OrderItemSerializer, ReviewSerializer, CartItemSerializer, ReferralProgramSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = NumberedPagePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReferralProgramViewSet(viewsets.ModelViewSet):
    queryset = ReferralProgram.objects.all()
    serializer_class = ReferralProgramSerializer
    permission_classes = [permissions.IsAdminUser]