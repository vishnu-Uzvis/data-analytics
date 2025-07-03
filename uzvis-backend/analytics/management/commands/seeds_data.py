from django.core.management.base import BaseCommand
from analytics.models import Users, Categories, Products, ProductVariants, Countries, Cities, Areas, Addresses, PromoCodes, Orders, OrderItems, WalletTransactions, Transactions, ReturnRequests
from datetime import datetime, timedelta
from random import choice, randint, uniform
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        ReturnRequests.objects.all().delete()
        Transactions.objects.all().delete()
        WalletTransactions.objects.all().delete()
        OrderItems.objects.all().delete()
        Orders.objects.all().delete()
        PromoCodes.objects.all().delete()
        Addresses.objects.all().delete()
        Areas.objects.all().delete()
        Cities.objects.all().delete()
        Countries.objects.all().delete()
        ProductVariants.objects.all().delete()
        Products.objects.all().delete()
        Categories.objects.all().delete()
        Users.objects.all().delete()

        # Seed Countries, Cities, Areas
        country = Countries.objects.create(name='India', iso2='IN', phone_code='+91')
        city = Cities.objects.create(name='Mumbai', country=country, latitude='19.0760', longitude='72.8777')
        area = Areas.objects.create(name='Bandra', city=city, latitude='19.0600', longitude='72.8300')

        # Seed Users
        users = [
            Users(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='hashed_password',  # In practice, hash passwords
                mobile=f'98765432{i:02d}',
                balance=uniform(100, 1000)
            ) for i in range(1, 11)
        ]
        Users.objects.bulk_create(users)

        # Seed Categories
        parent_cat = Categories.objects.create(name='Groceries', slug='groceries', image='groceries.jpg', city='Mumbai')
        child_cat = Categories.objects.create(name='Fruits', parent=parent_cat, slug='fruits', image='fruits.jpg', city='Mumbai')

        # Seed Products
        products = [
            Products(
                name=f'Product {i}',
                category=child_cat,
                slug=f'product-{i}',
                image=f'product{i}.jpg',
                price=uniform(50, 500),
                stock=randint(10, 100)
            ) for i in range(1, 21)
        ]
        Products.objects.bulk_create(products)

        # Seed Product Variants
        variants = []
        for product in Products.objects.all():
            variants.append(ProductVariants(
                product=product,
                price=product.price,
                stock=randint(5, 50)
            ))
        ProductVariants.objects.bulk_create(variants)

        # Seed Addresses
        addresses = [
            Addresses(
                user=user,
                address=f'Address {i}',
                area=area,
                city=city,
                pincode='400050',
                mobile=user.mobile
            ) for i, user in enumerate(users, 1)
        ]
        Addresses.objects.bulk_create(addresses)

        # Seed Promo Codes
        promo_codes = [
            PromoCodes(
                promo_code=f'PROMO{i:02d}',
                discount=uniform(5, 50),
                discount_type='percentage',
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=30)
            ) for i in range(1, 6)
        ]
        PromoCodes.objects.bulk_create(promo_codes)

        # Seed Orders
        statuses = ['pending', 'processing', 'delivered', 'cancelled']
        payment_methods = ['upi', 'cod', 'card', 'wallet']
        orders = []
        order_items = []
        transactions = []
        wallet_transactions = []
        return_requests = []

        for i in range(1, 101):
            user = choice(users)
            address = choice(addresses)
            promo = choice(promo_codes) if randint(0, 1) else None
            status = choice(statuses)
            payment_method = choice(payment_methods)
            order_date = timezone.now() - timedelta(days=randint(0, 180))
            total = uniform(100, 2000)
            promo_discount = total * (promo.discount / 100) if promo else 0
            final_total = total - promo_discount

            order = Orders(
                user=user,
                address=address,
                mobile=user.mobile,
                total=total,
                promo_code=promo,
                promo_discount=promo_discount,
                final_total=final_total,
                payment_method=payment_method,
                status=status,
                active_status=status,
                date_added=order_date,
                offer_type_details='{}',
                offer_discount=0
            )
            orders.append(order)

        Orders.objects.bulk_create(orders)

        # Seed Order Items
        for order in Orders.objects.all():
            variant = choice(ProductVariants.objects.all())
            quantity = randint(1, 5)
            order_items.append(OrderItems(
                user=order.user,
                order=order,
                product_name=variant.product.name,
                product_variant=variant,
                quantity=quantity,
                price=variant.price,
                sub_total=variant.price * quantity,
                status=order.status,
                active_status=order.status
            ))

        OrderItems.objects.bulk_create(order_items)

        # Seed Transactions
        for order in Orders.objects.all():
            if order.payment_method != 'cod':
                transactions.append(Transactions(
                    user=order.user,
                    order=order,
                    type='payment',
                    txn_id=f'TXN{i:03d}',
                    amount=order.final_total,
                    status='success',
                    currency_code='INR'
                ))

        Transactions.objects.bulk_create(transactions)

        # Seed Wallet Transactions
        for order in Orders.objects.filter(payment_method='wallet'):
            wallet_transactions.append(WalletTransactions(
                user=order.user,
                type='debit',
                amount=order.final_total,
                status='success'
            ))

        WalletTransactions.objects.bulk_create(wallet_transactions)

        # Seed Return Requests
        for order in Orders.objects.filter(status='delivered')[:10]:
            order_item = OrderItems.objects.filter(order=order).first()
            return_requests.append(ReturnRequests(
                user=order.user,
                order=order,
                order_item=order_item,
                return_request='Product defective',
                status='pending'
            ))

        ReturnRequests.objects.bulk_create(return_requests)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with sample data'))