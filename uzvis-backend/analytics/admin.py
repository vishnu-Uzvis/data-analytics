from django.contrib import admin
from .models import (
    Areas, Cities, Countries, Orders, ProductVariants, OrderItems,
    Transactions, ReturnRequests, Promocode, Users, Categories,
    Addresses, Products, WalletTransactions, Zipcodes
)

@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'zipcode', 'minimum_free_delivery_order_amount', 'delivery_charges')

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'iso2', 'capital', 'currency')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'date_added')
    list_filter = ('status', 'date_added')
    search_fields = ('id', 'user__username')
    list_per_page = 50

@admin.register(ProductVariants)
class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'stock', 'status')

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity', 'sub_total', 'status')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'user', 'order', 'amount', 'status')

@admin.register(ReturnRequests)
class ReturnRequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'status', 'date_created')

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'promo_code', 'discount', 'status', 'start_date', 'end_date')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'mobile', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'status')

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'type', 'mobile', 'pincode')

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'stock', 'status')
    search_fields = ('name',)

@admin.register(WalletTransactions)
class WalletTransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'amount', 'status', 'date_created')

@admin.register(Zipcodes)
class ZipcodesAdmin(admin.ModelAdmin):
    list_display = ('id', 'zipcode')