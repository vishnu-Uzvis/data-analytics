from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncDay
from .models import Orders, Transactions, OrderItems
from .serializers import KpiSerializer, OrderCountSerializer, RevenueSerializer, PaymentMethodSerializer, StatusBreakdownSerializer
from datetime import datetime
from dateutil.parser import parse

class AnalyticsView(APIView):
    def get(self, request):
        type_param = request.query_params.get('type')
        period = request.query_params.get('period', 'daily')
        date_range = request.query_params.get('date_range')
        status = request.query_params.get('status')
        payment_method = request.query_params.get('payment_method')
        location = request.query_params.get('location')

        queryset = Orders.objects.all()

        if date_range:
            try:
                start_date, end_date = date_range.split(',')
                start_date = parse(start_date).date()
                end_date = parse(end_date).date()
                queryset = queryset.filter(date_added__date__range=[start_date, end_date])
            except:
                return Response({'message': 'Invalid date range'}, status=status.HTTP_400_BAD_REQUEST)

        if status:
            queryset = queryset.filter(status=status)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if location:
            queryset = queryset.filter(address__pincode=location)

        if type_param == 'kpis':
            total_orders = queryset.count()
            net_revenue = queryset.aggregate(Sum('final_total'))['final_total__sum'] or 0
            avg_order_value = queryset.aggregate(Avg('final_total'))['final_total__avg'] or 0
            cancelled_orders = queryset.filter(status='cancelled').count()
            cancellation_rate = (cancelled_orders / total_orders * 100) if total_orders else 0
            avg_orders_per_period = queryset.count() / (end_date - start_date).days if date_range and total_orders else 0

            data = {
                'total_orders': total_orders,
                'net_revenue': net_revenue,
                'avg_order_value': avg_order_value,
                'cancellation_rate': cancellation_rate,
                'avg_orders_per_period': avg_orders_per_period
            }
            serializer = KpiSerializer(data)
            return Response({'data': serializer.data})

        elif type_param == 'count':
            if period == 'monthly':
                orders = queryset.annotate(period=TruncMonth('date_added')).values('period').annotate(count=Count('id')).order_by('period')
            else:
                orders = queryset.annotate(period=TruncDay('date_added')).values('period').annotate(count=Count('id')).order_by('period')
            serializer = OrderCountSerializer(orders, many=True)
            return Response({'data': serializer.data})

        elif type_param == 'revenue':
            if period == 'monthly':
                revenue = queryset.annotate(period=TruncMonth('date_added')).values('period').annotate(revenue=Sum('final_total')).order_by('period')
            else:
                revenue = queryset.annotate(period=TruncDay('date_added')).values('period').annotate(revenue=Sum('final_total')).order_by('period')
            serializer = RevenueSerializer(revenue, many=True)
            return Response({'data': serializer.data})

        elif type_param == 'payment_method':
            payments = queryset.values('payment_method').annotate(count=Count('payment_method')).order_by('payment_method')
            serializer = PaymentMethodSerializer(payments, many=True)
            return Response({'data': serializer.data})

        elif type_param == 'status_breakdown':
            serializer = StatusBreakdownSerializer(queryset, many=True)
            return Response({'data': serializer.data})

        return Response({'message': 'Invalid type parameter'}, status=status.HTTP_400_BAD_REQUEST)