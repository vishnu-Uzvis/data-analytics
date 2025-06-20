from rest_framework import serializers
from .models import Orders, Transactions, OrderItems

class KpiSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    net_revenue = serializers.FloatField()
    avg_order_value = serializers.FloatField()
    cancellation_rate = serializers.FloatField()
    avg_orders_per_period = serializers.FloatField()

class OrderCountSerializer(serializers.Serializer):
    period = serializers.CharField()
    count = serializers.IntegerField()

class RevenueSerializer(serializers.Serializer):
    period = serializers.CharField()
    revenue = serializers.FloatField()

class PaymentMethodSerializer(serializers.Serializer):
    method = serializers.CharField()
    count = serializers.IntegerField()

class StatusBreakdownSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='id')
    date = serializers.DateTimeField(source='date_added')
    delivery_date = serializers.DateField(source='delivery_date')
    payment_method = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        model = Orders
        fields = ['order_id', 'date', 'delivery_date', 'payment_method', 'status']