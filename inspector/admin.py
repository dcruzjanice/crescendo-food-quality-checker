# inspector/admin.py
from django.contrib import admin
from .models import Inspection

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('product', 'brand', 'improvements_needed', 'comments')
