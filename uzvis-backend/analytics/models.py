from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=45, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    image = models.TextField(blank=True)
    balance = models.FloatField(default=0)
    company = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    bonus_type = models.CharField(max_length=30, default='percentage_per_order')
    bonus = models.IntegerField(default=0)
    cash_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dob = models.CharField(max_length=16, blank=True)
    country_code = models.IntegerField(blank=True, null=True)
    city = models.TextField(blank=True)
    area = models.TextField(blank=True)
    street = models.TextField(blank=True)
    pincode = models.CharField(max_length=32, blank=True)
    apikey = models.CharField(max_length=32, blank=True)
    referral_code = models.CharField(max_length=32, blank=True)
    friends_code = models.CharField(max_length=28, blank=True)
    fcm_id = models.TextField(blank=True)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.CharField(max_length=256)
    image = models.TextField()
    banner = models.TextField(blank=True)
    row_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    clicks = models.IntegerField(default=0)
    city = models.TextField()

    def __str__(self):
        return self.name

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_identity = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    tax = models.FloatField(blank=True, null=True)
    row_order = models.IntegerField(default=0)
    type = models.CharField(max_length=34, blank=True)
    stock_type = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=512)
    short_description = models.TextField(blank=True)
    slug = models.CharField(max_length=512)
    indicator = models.SmallIntegerField(blank=True, null=True)
    cod_allowed = models.BooleanField(default=True)
    download_allowed = models.BooleanField(default=False)
    download_type = models.CharField(max_length=40, blank=True)
    download_link = models.CharField(max_length=512, blank=True)
    minimum_order_quantity = models.IntegerField(default=1)
    quantity_step_size = models.IntegerField(default=1)
    total_allowed_quantity = models.IntegerField(blank=True, null=True)
    is_prices_inclusive_tax = models.BooleanField(default=False)
    is_returnable = models.BooleanField(default=False)
    is_cancelable = models.BooleanField(default=False)
    cancelable_till = models.CharField(max_length=32, blank=True)
    is_attachment_required = models.BooleanField(default=False)
    image = models.TextField()
    other_images = models.TextField(blank=True)
    video_type = models.CharField(max_length=32, blank=True)
    video = models.CharField(max_length=512, blank=True)
    tags = models.TextField(blank=True)
    warranty_period = models.CharField(max_length=32, blank=True)
    guarantee_period = models.CharField(max_length=32, blank=True)
    made_in = models.CharField(max_length=128, blank=True)
    brand = models.CharField(max_length=256, blank=True)
    sku = models.CharField(max_length=128, blank=True)
    stock = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    no_of_ratings = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    deliverable_type = models.SmallIntegerField(default=1)
    deliverable_zipcodes = models.CharField(max_length=512, blank=True)
    city = models.TextField(blank=True)
    shipping_method = models.IntegerField(blank=True, null=True)
    pickup_location = models.CharField(max_length=512, blank=True)
    status = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_on_sale = models.BooleanField(default=False)
    sale_discount = models.IntegerField(default=0)
    sale_start_date = models.DateTimeField(blank=True, null=True)
    sale_end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProductVariants(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    attribute_value_ids = models.TextField(blank=True)
    attribute_set = models.CharField(max_length=255, blank=True)
    price = models.FloatField()
    special_price = models.FloatField(blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True)
    stock = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    breadth = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    images = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Variant"

class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=3, blank=True)
    iso2 = models.CharField(max_length=2, blank=True)
    phone_code = models.CharField(max_length=10, blank=True)
    capital = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

class Areas(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True)
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    pincode = models.CharField(max_length=10, blank=True)
    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Address"

class PromoCodes(models.Model):
    id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=28, unique=True)
    message = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_users = models.IntegerField(blank=True, null=True)
    minimum_order_amount = models.FloatField(blank=True, null=True)
    discount = models.FloatField()
    discount_type = models.CharField(max_length=50)
    max_discount_amount = models.FloatField(blank=True, null=True)
    repeat_usage = models.BooleanField(default=False)
    no_of_repeat_usage = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.promo_code

class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Wallet'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    delivery_boy_id = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=12)
    total = models.FloatField()
    delivery_charge = models.FloatField(default=0)
    is_delivery_charge_returnable = models.BooleanField(default=False)
    wallet_balance = models.FloatField(default=0)
    total_payable = models.FloatField(blank=True, null=True)
    promo_code = models.ForeignKey(PromoCodes, on_delete=models.SET_NULL, null=True, to_field='promo_code')
    promo_discount = models.FloatField(blank=True, null=True)
    discount = models.FloatField(default=0)
    final_total = models.FloatField()
    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES)
    latitude = models.CharField(max_length=256, blank=True)
    longitude = models.CharField(max_length=256, blank=True)
    address_text = models.TextField(blank=True)
    delivery_time = models.CharField(max_length=128, blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    active_status = models.CharField(max_length=16)
    date_added = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(default=0)
    email = models.EmailField(max_length=254, blank=True)
    notes = models.CharField(max_length=512, blank=True)
    attachments = models.TextField(blank=True)
    is_local_pickup = models.BooleanField(default=False)
    is_pos_order = models.BooleanField(default=False)
    seller_notes = models.TextField(blank=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    already_print_once = models.BooleanField(default=False)
    is_printed = models.BooleanField(default=False)
    offer_type_details = models.TextField()
    offer_discount = models.FloatField()
    city = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItems(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=512)
    variant_name = models.CharField(max_length=256, blank=True)
    product_variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    tax_percent = models.FloatField(blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    discount = models.FloatField(default=0)
    sub_total = models.FloatField()
    deliver_by = models.CharField(max_length=128, blank=True)
    updated_by = models.IntegerField(default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    active_status = models.CharField(max_length=16)
    hash_link = models.CharField(max_length=512, blank=True)
    is_sent = models.BooleanField(default=False)
    is_download = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} (Order {self.order.id})"

class WalletTransactions(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    amount = models.FloatField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.amount}"

class Transactions(models.Model):
    TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    txn_id = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    currency_code = models.CharField(max_length=10, blank=True)
    payer_email = models.EmailField(max_length=254, blank=True)
    message = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.txn_id} for Order {self.order.id}"

class ReturnRequests(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    return_request = models.TextField()
    user_reason = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for Order {self.order.id}"