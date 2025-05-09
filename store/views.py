from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.cart_utils import get_cart
from django.http import HttpResponseBadRequest
from .cart_utils import calculate_cart_total
from .forms import CustomUserCreationForm
from .forms import RegisterForm
from store.utils.email_utils import send_order_confirmation_email
from django.core.paginator import Paginator
import pandas as pd
from .forms import ProductUploadForm

def bulk_upload_products(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                df = pd.read_excel(excel_file)
                for _, row in df.iterrows():
                    Product.objects.create(
                        name=row['name'],
                        price=row['price'],
                        description=row.get('description', '')
                    )
                return redirect('product_list')  # or any success page
            except Exception as e:
                return render(request, 'store/bulk_upload.html', {'form': form, 'error': str(e)})
    else:
        form = ProductUploadForm()
    
    return render(request, 'store/bulk_upload.html',{'form':form})

from .models import Product, Category
from django.core.paginator import Paginator

def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search and filter
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category_id=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # change as needed
    else:
        form = RegisterForm()
    return render(request, 'store/register.html',{'form':form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "store/register.html", {"form": form})

def calculate_cart_total(user):
    cart_items = get_cart(user)
    return sum(item.product.price * item.quantity for item in cart_items)
def place_order(request):
    if request.method == "POST":
        total = calculate_cart_total(request.user)
        order = Order.objects.create(user=request.user, total_amount=total)

        print("User email is:", request.user.email)  # <--- add this line

        try:
            send_mail(
                subject=f'Order Confirmation #{order.id} Total: {order.total_amount}',
                message='Thank you for your order!',
                from_email='rahipatel03@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            print("Mail sent!")
        except Exception as e:
            print("Mail failed:", e)

        return redirect("order_success")
@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def pay_now(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    if request.method == 'POST':
        order.is_paid = True
        order.save()
        return redirect('order_detail', order_id=order.id)
    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')

def checkout_view(request):
    if request.method == 'POST':
        # calculate the total
        total_price = calculate_cart_total(request)  # use your own logic

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            # Add any other fields like address, items, etc.
        )

        # Send confirmation email
        send_order_confirmation_email(order, request.user.email)

        return redirect('order_success')  # Or wherever you redirect after order

def home_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__iexact=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })

from django.db.models import Q

def home(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    q = request.GET.get('q')

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if q:
        products = products.filter(Q(name_icontains=q) | Q(description_icontains=q))

    return render(request, 'store/home.html', {'categories': categories, 'products': products})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)
    return render(request, 'store/cart.html', {'products': products, 'cart': cart, 'total': total})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})
