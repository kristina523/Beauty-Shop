from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    bonus_points = models.IntegerField(default=0)
    personal_discount = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True, db_column='parent_id')

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, models.CASCADE, db_column='category_id')
    brand = models.ForeignKey(Brand, models.CASCADE, blank=True, null=True, db_column='brand_id')
    stock_quantity = models.IntegerField(default=0)
    image_url = models.URLField('Ссылка на изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_best_seller = models.BooleanField(default=False)
    sales_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='user_id')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='new')
    delivery_address = models.TextField()

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.CASCADE, db_column='order_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    user = models.ForeignKey(User, models.CASCADE, db_column='user_id')
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        unique_together = (('product', 'user'),)

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='user_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart'
        unique_together = (('user', 'product'),)

    def get_cost(self):
        return (self.product.discounted_price or self.product.price) * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class ReferralProgram(models.Model):
    referral_id = models.AutoField(primary_key=True)
    referrer = models.ForeignKey(User, models.CASCADE, db_column='referrer_id', related_name='referrals_made')
    referred = models.ForeignKey(User, models.CASCADE, db_column='referred_id', related_name='referrals_received')
    referral_date = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'referral_program'
        unique_together = (('referred',),)

