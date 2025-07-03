from rest_framework import serializers

class KpiSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    net_revenue = serializers.FloatField()
    avg_order_value = serializers.FloatField()
    cancellation_rate = serializers.FloatField()
    avg_orders_per_period = serializers.FloatField()

class OrderCountSerializer(serializers.Serializer):
    period = serializers.DateField(help_text="Date corresponding to the period aggregation")
    count = serializers.IntegerField()

class RevenueSerializer(serializers.Serializer):
    period = serializers.DateField(help_text="Date corresponding to revenue aggregation")
    revenue = serializers.FloatField()

class PaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    count = serializers.IntegerField()

class StatusBreakdownSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()

class RevenueDetailSerializer(serializers.Serializer):
    """
    Serializer for detailed revenue breakdown grouped by product or category.
    """
    group = serializers.CharField(help_text="Product name or category name")
    variant_name = serializers.CharField(help_text="Name of the product variant")
    total_quantity = serializers.IntegerField(help_text="Total units sold in the period")
    price_per_unit = serializers.FloatField(help_text="Price per single unit of the variant")
    total_price = serializers.FloatField(help_text="Total revenue for the variant or category")
