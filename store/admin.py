from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Category, Order

# Extend UserAdmin to show email
class CustomUserAdmin(UserAdmin):
    # Show email in list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    # Add email to fieldsets only if it's not already there
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Unregister default User and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)