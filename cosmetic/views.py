from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Category, CartItem, Review, User, Order, OrderItem
from django.db.models import Count
from .forms import ProductForm, ReviewForm, RegistrationForm, CustomLoginForm
from .forms import ProfileImageForm

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
    return render(request, 'cosmetic/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'cosmetic/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

def reviews(request):
    all_reviews = Review.objects.all().select_related('user', 'product')
    context = {
        'title': 'Отзывы наших клиентов',
        'reviews': all_reviews
    }
    return render(request, 'cosmetic/reviews.html', context)

def promotions(request):
    return render(request, 'cosmetic/promotions.html')

def new_products(request):
    new_products = Product.objects.filter(is_best_seller=True)
    return render(request, 'cosmetic/new_products.html', {
        'title': 'Новинки',
        'new_products': new_products
    })

def best_sellers(request):
    best_sellers = Product.objects.order_by('-sales_count')[:12]
    context = {
        'title': 'Хиты продаж',
        'best_sellers': best_sellers
    }
    return render(request, 'cosmetic/best_sellers.html', context)

def product_add(request):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cosmetic:product_list')
    else:
        form = ProductForm()
    return render(request, 'cosmetic/product_form.html', {'form': form, 'title': 'Добавить товар'})

def product_edit(request, product_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('cosmetic:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'cosmetic/product_form.html', {'form': form, 'title': 'Изменить товар'})

def product_delete(request, product_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('cosmetic:product_list')
    return render(request, 'cosmetic/product_confirm_delete.html', {'product': product})

def add_to_cart(request, product_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    product = get_object_or_404(Product, product_id=product_id)
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_item, created = CartItem.objects.get_or_create(
        user=custom_user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cosmetic:cart')

def cart_view(request):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_items = CartItem.objects.filter(user=custom_user)
    total_price = sum(item.get_cost() for item in cart_items)
    return render(request, 'cosmetic/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def remove_from_cart(request, item_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_item = get_object_or_404(CartItem, pk=item_id, user=custom_user)
    cart_item.delete()
    return redirect('cosmetic:cart')

def clear_cart(request):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_items = CartItem.objects.filter(user=custom_user)
    cart_items.delete()
    return redirect('cosmetic:cart')

def update_cart_item(request, item_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_item = get_object_or_404(CartItem, pk=item_id, user=custom_user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cosmetic:cart')

def add_review(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        # обработка неавторизованного пользователя
        return redirect('cosmetic:login')

    # Проверяем, есть ли уже отзыв
    existing_review = Review.objects.filter(product_id=product_id, user_id=user_id).first()
    if existing_review:
        # Можно показать сообщение или редиректить
        messages.error(request, "Вы уже оставили отзыв на этот товар.")
        return redirect('cosmetic:product_detail', product_id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user_id = user_id
            review.save()
            messages.success(request, "Спасибо за ваш отзыв!")
            return redirect('cosmetic:product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'cosmetic/add_review.html', {'form': form})

def checkout(request):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=request.session['user_id'])
    cart_items = CartItem.objects.filter(user=custom_user)
    if not cart_items.exists():
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cosmetic:cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            messages.error(request, "Пожалуйста, укажите адрес доставки.")
            return redirect('cosmetic:checkout')

        total = sum(item.get_cost() for item in cart_items)
        order = Order.objects.create(
            user=custom_user,
            total_amount=total,
            status='new',
            delivery_address=address
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.discounted_price or item.product.price
            )
        cart_items.delete()
        messages.success(request, "Заказ успешно оформлен!")
        return redirect('cosmetic:order_success', order_id=order.order_id)

    return render(request, 'cosmetic/checkout.html', {
        'cart_items': cart_items,
        'total_price': sum(item.get_cost() for item in cart_items),
    })

def order_success(request, order_id):
    if not request.session.get('user_id'):
        return redirect('cosmetic:login')
    return render(request, 'cosmetic/order_success.html', {'order_id': order_id})

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('cosmetic:login')
    custom_user = User.objects.get(user_id=user_id)
    orders = Order.objects.filter(user=custom_user).order_by('-order_date')

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=custom_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фото профиля обновлено!')
            return redirect('cosmetic:profile')
    else:
        form = ProfileImageForm(instance=custom_user)

    context = {
        'user': custom_user,
        'orders': orders,
        'form': form,
    }
    return render(request, 'cosmetic/profile.html', context)

def delivery(request):
    return render(request, 'cosmetic/delivery.html')

def payment(request):
    return render(request, 'cosmetic/payment.html')

def guarantee(request):
    return render(request, 'cosmetic/guarantee.html')

def blog(request):
    return render(request, 'cosmetic/blog.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            import hashlib
            user.password_hash = hashlib.sha256(form.cleaned_data['password'].encode()).hexdigest()
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('cosmetic:login')
    else:
        form = RegistrationForm()
    return render(request, 'cosmetic/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                user = User.objects.get(username=username)
                if user.password_hash == password_hash:
                    request.session['user_id'] = user.user_id
                    request.session['username'] = user.username
                    return redirect('cosmetic:home')
                else:
                    error = 'Неверный пароль'
            except User.DoesNotExist:
                error = 'Пользователь не найден'
    else:
        form = CustomLoginForm()
    return render(request, 'cosmetic/login.html', {'form': form, 'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('cosmetic:home')