from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Cost_of_sales)
class Cost_of_goodsAdmin(admin.ModelAdmin):
    list_display=[
        'name', 'category','amount', 'description', 'date'
        
    ]
    search_fields = [
        'name', 'category', 'date'
    ]

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location', 'value', 'date_acquired'

    ]
    search_fields = [
        'name', 'date_acquired'
    ]


@admin.register(Liability)
class LiabilityAmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'due_date']
    search_fields = ['name', 'due_date']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'amount', 'drawn_by', 'date']
    search_fields = ['category', 'date', 'drawn_by']


@admin.register(Revenue)
class RevunueAdmin(admin.ModelAdmin):
    list_display = ['category', 'description',
                    'amount', 'received_from', 'date']
    search_fields = ['category', 'date', 'received_from']
