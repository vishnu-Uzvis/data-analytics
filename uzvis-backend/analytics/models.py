from django.db import models

class Areas(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, db_column='city_id')
    zipcode = models.ForeignKey('Zipcodes', on_delete=models.CASCADE, db_column='zipcode_id', null=True)
    minimum_free_delivery_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charges = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'areas'
        managed = False

class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'cities'
        managed = False

class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=3)
    numeric_code = models.CharField(max_length=3)
    iso2 = models.CharField(max_length=2)
    phonecode = models.CharField(max_length=10)
    capital = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=10)
    tld = models.CharField(max_length=10)
    native = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    subregion = models.CharField(max_length=255)
    timezones = models.TextField()
    translations = models.TextField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    emoji = models.CharField(max_length=255)
    emojiU = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    flag = models.IntegerField()
    wikiDataId = models.CharField(max_length=255)

    class Meta:
        db_table = 'countries'
        managed = False

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id', related_name='user_orders')
    delivery_boy = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, db_column='delivery_boy_id', related_name='delivery_orders')
    address = models.ForeignKey('Addresses', on_delete=models.SET_NULL, null=True, db_column='address_id')
    mobile = models.CharField(max_length=12)
    total = models.FloatField()
    delivery_charge = models.FloatField(default=0)
    is_delivery_charge_returnable = models.BooleanField(default=False)
    wallet_balance = models.FloatField(default=0)
    total_payable = models.FloatField(null=True)
    promo_code = models.ForeignKey('Promocode', on_delete=models.SET_NULL, null=True, to_field='promo_code', db_column='promo_code')
    promo_discount = models.FloatField(null=True)
    discount = models.FloatField(default=0)
    final_total = models.FloatField(null=True)
    payment_method = models.CharField(max_length=16)
    latitude = models.CharField(max_length=256, null=True)
    longitude = models.CharField(max_length=256, null=True)
    address_text = models.TextField(db_column='address', null=True)
    delivery_time = models.CharField(max_length=128, null=True)
    delivery_date = models.DateField(null=True)
    status = models.CharField(max_length=1024)
    active_status = models.CharField(max_length=16)
    date_added = models.DateTimeField()
    otp = models.IntegerField(default=0)
    email = models.EmailField(null=True)
    notes = models.CharField(max_length=512, null=True)
    attachments = models.CharField(max_length=2048, null=True)
    is_local_pickup = models.BooleanField(default=False)
    is_pos_order = models.BooleanField(default=False)
    seller_notes = models.TextField(null=True)
    pickup_time = models.DateTimeField(null=True)
    already_print_once = models.BooleanField(default=False)
    is_printed = models.IntegerField(null=True)
    offer_type_details = models.TextField()
    offer_discount = models.FloatField()
    # Changed to match actual column name 'city'
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, db_column='city')

    class Meta:
        db_table = 'orders'
        managed = False

class ProductVariants(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, db_column='product_id')
    attribute_value_ids = models.TextField(null=True)
    attribute_set = models.CharField(max_length=1024, null=True)
    price = models.FloatField()
    special_price = models.FloatField(default=0, null=True)
    sku = models.CharField(max_length=128, null=True)
    stock = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField()
    breadth = models.FloatField()
    length = models.FloatField()
    images = models.TextField(null=True)
    # Changed availability to IntegerField to match tinyint values
    availability = models.IntegerField(null=True)
    # Changed status to IntegerField to match tinyint values
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField()

    class Meta:
        db_table = 'product_variants'
        managed = False

class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='order_id')
    product_name = models.CharField(max_length=512, null=True)
    variant_name = models.CharField(max_length=256, null=True)
    product_variant = models.ForeignKey('ProductVariants', on_delete=models.CASCADE, db_column='product_variant_id')
    quantity = models.IntegerField()
    price = models.FloatField()
    discounted_price = models.FloatField(null=True)
    tax_percent = models.FloatField(null=True)
    tax_amount = models.FloatField(null=True)
    discount = models.FloatField(default=0)
    sub_total = models.FloatField()
    deliver_by = models.CharField(max_length=128, null=True)
    updated_by = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=1024)
    active_status = models.CharField(max_length=16)
    hash_link = models.CharField(max_length=512, null=True)
    is_sent = models.BooleanField(default=False)
    is_download = models.BooleanField(default=False)
    date_added = models.DateTimeField()

    class Meta:
        db_table = 'order_items'
        managed = False

class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=16)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='order_id')
    order_item = models.ForeignKey('OrderItems', on_delete=models.CASCADE, null=True, db_column='order_item_id')
    type = models.CharField(max_length=64, null=True)
    txn_id = models.CharField(max_length=256, null=True)
    payu_txn_id = models.CharField(max_length=512, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=12, null=True)
    currency_code = models.CharField(max_length=5, null=True)
    payer_email = models.CharField(max_length=64, null=True)
    message = models.CharField(max_length=128)
    transaction_date = models.DateTimeField(null=True)
    date_created = models.DateTimeField()
    is_refund = models.BooleanField(default=False)

    class Meta:
        db_table = 'transactions'
        managed = False

class ReturnRequests(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, db_column='product_id')
    product_variant = models.ForeignKey('ProductVariants', on_delete=models.CASCADE, db_column='product_variant_id')
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='order_id')
    order_item = models.ForeignKey('OrderItems', on_delete=models.CASCADE, db_column='order_item_id')
    # Changed status from BooleanField to IntegerField to match actual DB values
    status = models.IntegerField()
    remarks = models.CharField(max_length=1024, null=True)
    date_created = models.DateTimeField()

    class Meta:
        db_table = 'return_requests'
        managed = False

class Promocode(models.Model):
    id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=28, unique=True)
    message = models.CharField(max_length=512, null=True)
    start_date = models.CharField(max_length=28, null=True)
    end_date = models.CharField(max_length=28, null=True)
    no_of_users = models.IntegerField(null=True)
    minimum_order_amount = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    discount_type = models.CharField(max_length=32, null=True)
    max_discount_amount = models.FloatField(null=True)
    repeat_usage = models.IntegerField()
    no_of_repeat_usage = models.IntegerField(null=True)
    image = models.CharField(max_length=256, null=True)
    status = models.IntegerField()
    is_cashback = models.IntegerField(default=0)
    list_promocode = models.IntegerField(default=1)
    is_specific_users = models.IntegerField(default=0)
    users_id = models.CharField(max_length=256)
    date_created = models.DateTimeField()

    class Meta:
        db_table = 'promo_codes'
        managed = False

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=45, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20, null=True)
    image = models.TextField(null=True)
    balance = models.FloatField(default=0)
    activation_selector = models.CharField(max_length=255, null=True)
    activation_code = models.CharField(max_length=255, null=True)
    forgotten_password_selector = models.CharField(max_length=255, null=True)
    forgotten_password_code = models.CharField(max_length=255, null=True)
    forgotten_password_time = models.IntegerField(null=True)
    remember_selector = models.CharField(max_length=255, null=True)
    remember_code = models.CharField(max_length=255, null=True)
    created_on = models.IntegerField()
    last_login = models.IntegerField(null=True)
    active = models.BooleanField(null=True)
    company = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    bonus_type = models.CharField(max_length=30, null=True, default='percentage_per_order')
    bonus = models.IntegerField(null=True)
    cash_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dob = models.CharField(max_length=16, null=True)
    country_code = models.IntegerField(null=True)
    city = models.TextField(null=True)
    area = models.TextField(null=True)
    street = models.TextField(null=True)
    pincode = models.CharField(max_length=32, null=True)
    apikey = models.CharField(max_length=32, null=True)
    referral_code = models.CharField(max_length=32, null=True)
    friends_code = models.CharField(max_length=28, null=True)
    fcm_id = models.TextField(null=True)
    latitude = models.CharField(max_length=64, null=True)
    longitude = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'
        managed = False

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, db_column='parent_id')
    slug = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    banner = models.CharField(max_length=255, null=True)
    row_order = models.IntegerField()
    status = models.BooleanField()
    clicks = models.IntegerField()
    city = models.IntegerField(null=True)

    class Meta:
        db_table = 'categories'
        managed = False

class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    name = models.CharField(max_length=64, null=True)
    type = models.CharField(max_length=32, null=True)
    mobile = models.CharField(max_length=24, null=True)
    alternate_mobile = models.CharField(max_length=24, null=True)
    address = models.TextField(null=True)
    landmark = models.CharField(max_length=255, null=True)
    area = models.ForeignKey('Areas', on_delete=models.SET_NULL, null=True, db_column='area_id')
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, db_column='city_id')
    city_text = models.CharField(max_length=256, null=True, db_column='city')
    area_text = models.CharField(max_length=256, null=True, db_column='area')
    pincode = models.CharField(max_length=512, null=True)
    country_code = models.IntegerField(null=True)
    state = models.CharField(max_length=64, null=True)
    country = models.CharField(max_length=64, null=True)
    latitude = models.CharField(max_length=64, null=True)
    longitude = models.CharField(max_length=64, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'
        managed = False

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_identity = models.CharField(max_length=255)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, db_column='category_id')
    tax = models.FloatField(null=True)
    row_order = models.IntegerField()
    type = models.CharField(max_length=50)
    stock_type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    slug = models.CharField(max_length=255)
    indicator = models.CharField(max_length=50, null=True)
    cod_allowed = models.BooleanField()
    download_allowed = models.BooleanField()
    download_type = models.CharField(max_length=50, null=True)
    download_link = models.CharField(max_length=255, null=True)
    minimum_order_quantity = models.IntegerField()
    quantity_step_size = models.IntegerField()
    total_allowed_quantity = models.IntegerField()
    is_prices_inclusive_tax = models.BooleanField()
    is_returnable = models.BooleanField()
    is_cancelable = models.BooleanField()
    cancelable_till = models.CharField(max_length=50, null=True)
    is_attachment_required = models.BooleanField()
    image = models.CharField(max_length=255)
    other_images = models.TextField(null=True)
    video_type = models.CharField(max_length=50, null=True)
    video = models.CharField(max_length=255, null=True)
    tags = models.TextField(null=True)
    warranty_period = models.CharField(max_length=50, null=True)
    guarantee_period = models.CharField(max_length=50, null=True)
    made_in = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    sku = models.CharField(max_length=255)
    stock = models.IntegerField()
    availability = models.BooleanField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    no_of_ratings = models.IntegerField()
    description = models.TextField()
    deliverable_type = models.CharField(max_length=50)
    deliverable_zipcodes = models.TextField(null=True)
    city = models.CharField(max_length=255, null=True)
    shipping_method = models.CharField(max_length=50, null=True)
    pickup_location = models.CharField(max_length=255, null=True)
    status = models.BooleanField()
    date_added = models.DateTimeField()
    is_on_sale = models.BooleanField()
    sale_discount = models.FloatField(null=True)
    sale_start_date = models.DateTimeField(null=True)
    sale_end_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'products'
        managed = False

class WalletTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=8)
    amount = models.FloatField()
    message = models.CharField(max_length=512)
    status = models.BooleanField()
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'wallet_transactions'
        managed = False

class Zipcodes(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.CharField(max_length=20)

    class Meta:
        db_table = 'zipcodes'
        managed = False

# Revenue / Sold and Purchased summary based on raw SQL aggregation
class RevenueSummary(models.Model):
    delivery_date = models.DateField()
    product_name = models.CharField(max_length=512)
    variant_name = models.CharField(max_length=256)
    total_quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField()
    VE00_Total = models.FloatField()
    FR00_Total = models.FloatField()
    CH00_Total = models.FloatField()
    DR00_Total = models.FloatField()
    SP00_Total = models.FloatField()
    CC00_Total = models.FloatField()
    RE00_Total = models.FloatField()
    JU00_Total = models.FloatField()
    MS00_Total = models.FloatField()
    MT00_Total = models.FloatField()
    VP00_Total = models.FloatField()
    NV00_Total = models.FloatField()
    CO00_Total = models.FloatField()
    PU00_Total = models.FloatField()
    GR00_Total = models.FloatField()
    NC00_Total = models.FloatField()
    MU00_Total = models.FloatField()
    DP00_Total = models.FloatField()
    PI00_Total = models.FloatField()

    class Meta:
        # Assuming you've created a DB view named 'revenue_summary_view'
        db_table = 'revenue_summary_view'
        managed = False
