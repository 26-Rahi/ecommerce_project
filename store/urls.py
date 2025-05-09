from django.urls import path
from . import views
from .views import bulk_upload_products

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.view_cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('admin/add-product/', views.add_product, name='add_product'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('pay/<int:order_id>/', views.pay_now, name='pay_now'),
    path('order-success/', views.order_success, name='order_success'),
    path('products/', views.product_list_view, name='product_list'),
    path('bulk-upload/', bulk_upload_products, name='bulk_upload_products'),
]

