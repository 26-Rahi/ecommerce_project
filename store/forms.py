from django import forms
from .models import Order
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['full_name', 'address','city','postal_code','phone']

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'pattern': '^[A-Z0-9]{8}$',
            'title': 'Password must be exactly 8 characters long with uppercase letters and numbers only.',
            'maxlength': '8',
            'minlength': '8',
        }),
        help_text='Password must be exactly 8 characters with only uppercase letters and numbers.'
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.fullmatch(r'[A-Z0-9]{8}', password):
            raise forms.ValidationError('Password must be exactly 8 characters long with only uppercase letters and numbers.')
        return password

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']

class ProductUploadForm(forms.Form):
    file = forms.FileField()    