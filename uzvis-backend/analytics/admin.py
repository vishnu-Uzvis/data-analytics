from django.contrib import admin
from .models import Users, Categories, Products, ProductVariants, Countries, Cities, Areas, Addresses, PromoCodes, Orders, OrderItems, WalletTransactions, Transactions, ReturnRequests

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'created_at')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'status')

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'status')

@admin.register(ProductVariants)
class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'stock')

@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso2')

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'pincode')

@admin.register(PromoCodes)
class PromoCodesAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'discount', 'status')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'date_added')

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'sub_total')

@admin.register(WalletTransactions)
class WalletTransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'status')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('txn_id', 'order', 'amount', 'status')

@admin.register(ReturnRequests)
class ReturnRequestsAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'status')