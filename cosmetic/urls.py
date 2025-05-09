from django.urls import path
from django.contrib.auth import views as auth_views  
from . import views

app_name = 'cosmetic'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('map/', views.map, name='map'),
    path('blog/', views.blog, name='blog'),
    path('promotions/', views.promotions, name='promotions'),
    path('new-products/', views.new_products, name='new_products'),
    path('best-sellers/', views.best_sellers, name='best_sellers'),
    path('reviews/', views.reviews, name='reviews'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('delivery/', views.delivery, name='delivery'),
    path('payment/', views.payment, name='payment'),
    path('guarantee/', views.guarantee, name='guarantee'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
]