from django.contrib import admin
from .models import BrandProfile

class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_approved', 'is_verified', 'is_validated', 'created_at')  # Add 'is_validated' to list_display
    list_filter = ('is_approved', 'is_verified', 'is_validated', 'created_at')  # Add 'is_validated' to list_filter
    search_fields = ('user__username', 'name', 'address', 'district', 'pincode', 'state', 'fssai_no')

admin.site.register(BrandProfile, BrandProfileAdmin)
