from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description', 'type', 'amount_pence')
    search_fields = ['description']
    list_filter = ('type', 'date')
