from django import forms
from .models import Order, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError
# Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'city', 'postal_code', 'phone']


# Custom User Creation Form with Password Restrictions
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number.")
        return password
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Register Form (extends UserCreationForm and uses cleaned email)
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


# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']


# Product Upload Form for Bulk Upload
class ProductUploadForm(forms.Form):
    file = forms.FileField()