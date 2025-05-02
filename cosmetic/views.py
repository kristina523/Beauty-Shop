from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Review

def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'cosmetic/home.html', {'products': products})

def about(request):
    return render(request, 'cosmetic/about.html')

def contacts(request):
    return render(request, 'cosmetic/contacts.html')

def map(request):
    return render(request, 'cosmetic/map.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': int(category_id) if category_id else None
    }
    return render(request, 'cosmetic/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')
    context = {
        'product': product,
        'reviews': reviews,
        'review_choices': Review.RATING_CHOICES,
    }
    return render(request, 'cosmetic/product_detail.html', context)

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        Review.objects.create(
            product=product,
            user=request.user,
            name=request.user.get_full_name() or request.user.username,
            rating=request.POST.get('rating'),
            text=request.POST.get('text')
        )
    return redirect('cosmetic:product_detail', product_id=product_id)

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('product')
    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cosmetic/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cosmetic:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cosmetic:cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'total': cart_item.cart.get_total_price(),
        'item_total': cart_item.get_cost()
    })
@login_required
def profile_view(request):
    
    
    context = {
        'user': request.user,
    }
    return render(request, 'cosmetic/profile.html', context)
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('cosmetic:cart')

def delivery(request):
    return render(request, 'cosmetic/delivery.html')

def payment(request):
    return render(request, 'cosmetic/payment.html')

def guarantee(request):
    return render(request, 'cosmetic/guarantee.html')

def blog(request):
    return render(request, 'cosmetic/blog.html')