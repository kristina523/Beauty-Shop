from django import forms
from .models import Product, Review, Order, User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'discounted_price',
            'category', 'brand', 'stock_quantity', 'image_url', 'is_best_seller'
        ]

RATING_CHOICES = [
    (5, '★★★★★'),
    (4, '★★★★☆'),
    (3, '★★★☆☆'),
    (2, '★★☆☆☆'),
    (1, '★☆☆☆☆'),
]

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_amount', 'status', 'delivery_address']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Пароли не совпадают")
        return cleaned_data

class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']