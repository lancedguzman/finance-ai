from django.contrib import admin
from .models import Transaction, Category

class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model."""
    list_display = ('transaction_id', 'date', 'amount', 'category')
    list_filter = ('date', 'category')
    search_fields = ('category__name',)


class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
