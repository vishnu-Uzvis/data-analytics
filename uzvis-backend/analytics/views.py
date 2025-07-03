from django.db.models import Min, Max, Count, Sum, Avg, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dateutil.parser import parse
import logging
from datetime import date

from .models import Orders, OrderItems, ProductVariants, Products, Categories
from .serializers import (
    KpiSerializer,
    OrderCountSerializer,
    RevenueSerializer,
    PaymentMethodSerializer,
    StatusBreakdownSerializer,
    RevenueDetailSerializer,  # Serializer for detailed revenue
)

logger = logging.getLogger(__name__)

class BaseAnalyticsView(APIView):
    def apply_filters(self, queryset, request, date_field='delivery_date'):
        """
        Applies status, payment_method, location filters and date range on given date_field.
        Returns: (filtered_qs, date_range, start_date, end_date)
        """
        date_range = request.query_params.get('date_range')
        order_status = request.query_params.get('status')
        payment_method = request.query_params.get('payment_method')
        location = request.query_params.get('location')

        start_date = end_date = date.today()
        if date_range:
            try:
                start_str, end_str = date_range.split(',')
                start_date = parse(start_str).date()
                end_date = parse(end_str).date()
                lookup = f"{date_field}__range"
                queryset = queryset.filter(**{lookup: [start_date, end_date]})
            except Exception as exc:
                logger.error(f"Invalid date range `{date_range}`: {exc}")
                raise ValueError("Invalid date range format. Use YYYY-MM-DD,YYYY-MM-DD")

        if order_status:
            queryset = queryset.filter(status=order_status)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if location:
            queryset = queryset.filter(address__pincode=location)

        return queryset, date_range, start_date, end_date

class KpisView(BaseAnalyticsView):
    def get(self, request):
        try:
            qs = Orders.objects.select_related('address', 'user').all()
            qs, date_range, start_date, end_date = self.apply_filters(qs, request)

            total_orders = qs.count()
            net_revenue = qs.aggregate(total=Sum('final_total'))['total'] or 0
            avg_order_value = qs.aggregate(avg=Avg('final_total'))['avg'] or 0

            cancelled = qs.filter(status='cancelled').count()
            cancellation_rate = (cancelled / total_orders * 100) if total_orders else 0

            days = (end_date - start_date).days or 1
            avg_orders_per_day = total_orders / days

            metrics = {
                'total_orders': total_orders,
                'net_revenue': float(net_revenue),
                'avg_order_value': float(avg_order_value),
                'cancellation_rate': float(cancellation_rate),
                'avg_orders_per_period': float(avg_orders_per_day),
            }

            serializer = KpiSerializer(data=metrics)
            serializer.is_valid(raise_exception=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in KpisView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderCountView(BaseAnalyticsView):
    def get(self, request):
        try:
            period = request.query_params.get('period', 'daily')
            qs = Orders.objects.select_related('address').all()
            qs, *_ = self.apply_filters(qs, request)
            qs = qs.exclude(delivery_date__isnull=True)

            if period == 'monthly':
                qs = qs.annotate(period=TruncMonth('delivery_date'))
            elif period == 'weekly':
                qs = qs.annotate(period=TruncWeek('delivery_date'))
            else:
                qs = qs.annotate(period=TruncDay('delivery_date'))

            counts = qs.values('period').annotate(count=Count('id')).order_by('period')
            if not counts:
                return Response({'data': [], 'message': 'No orders with delivery dates available.'}, status=status.HTTP_200_OK)

            cleaned = [
                {'period': obj['period'].date() if hasattr(obj['period'], 'date') else obj['period'], 'count': obj['count']}
                for obj in counts
            ]

            serializer = OrderCountSerializer(cleaned, many=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in OrderCountView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RevenueView(BaseAnalyticsView):
    def get(self, request):
        try:
            period = request.query_params.get('period', 'daily')
            qs = Orders.objects.select_related('address').all()
            qs, *_ = self.apply_filters(qs, request)
            qs = qs.exclude(delivery_date__isnull=True)

            if period == 'monthly':
                qs = qs.annotate(period=TruncMonth('delivery_date'))
            elif period == 'weekly':
                qs = qs.annotate(period=TruncWeek('delivery_date'))
            else:
                qs = qs.annotate(period=TruncDay('delivery_date'))

            rev = qs.values('period').annotate(revenue=Sum('final_total')).order_by('period')
            if not rev:
                return Response({'data': [], 'message': 'No revenue data available.'}, status=status.HTTP_200_OK)

            cleaned = [
                {'period': obj['period'].date() if hasattr(obj['period'], 'date') else obj['period'], 'revenue': obj['revenue']}
                for obj in rev
            ]

            serializer = RevenueSerializer(cleaned, many=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in RevenueView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RevenueDetailView(BaseAnalyticsView):
    """
    GET /analytics/revenue-details/?date_range=YYYY-MM-DD,YYYY-MM-DD
                                   &group_by={product|category}
                                   &category=<id or name>
                                   &product=<id or name>
    """
    def get(self, request):
        try:
            order_qs = Orders.objects.all()
            order_qs, _, start_date, end_date = self.apply_filters(order_qs, request)
            order_qs = order_qs.exclude(delivery_date__isnull=True)

            items = OrderItems.objects.filter(
                order__in=order_qs,
                active_status__startswith='d'
            ).select_related(
                'product_variant__product__category'
            )

            cat = request.query_params.get('category')
            if cat:
                items = items.filter(
                    product_variant__product__category__id=cat
                ) | items.filter(
                    product_variant__product__category__name__icontains=cat
                )

            prod = request.query_params.get('product')
            if prod:
                items = items.filter(
                    product_variant__product__id=prod
                ) | items.filter(
                    product_name__icontains=prod
                )

            group = request.query_params.get('group_by', 'product').lower()
            if group == 'category':
                key = 'product_variant__product__category__name'
            else:
                key = 'product_name'

            qs = items.values(key, 'variant_name').annotate(
                total_quantity=Sum('quantity'),
                price_per_unit=Max('price'),
                total_price=Sum('sub_total'),
            ).order_by(key)

            cleaned = []
            for obj in qs:
                cleaned.append({
                    'group': obj[key],
                    'variant_name': obj['variant_name'],
                    'total_quantity': obj['total_quantity'],
                    'price_per_unit': obj['price_per_unit'],
                    'total_price': obj['total_price'],
                })

            serializer = RevenueDetailSerializer(cleaned, many=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in RevenueDetailView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentMethodsView(BaseAnalyticsView):
    def get(self, request):
        try:
            qs = Orders.objects.select_related('address').all()
            qs, *_ = self.apply_filters(qs, request)

            payments = qs.values('payment_method').annotate(count=Count('id')).order_by('payment_method')
            if not payments:
                payments = [{'payment_method': m, 'count': 0} for m in ['upi', 'cod', 'card', 'wallet']]

            serializer = PaymentMethodSerializer(payments, many=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in PaymentMethodsView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatusBreakdownView(BaseAnalyticsView):
    def get(self, request):
        try:
            qs = Orders.objects.select_related('address').all()
            qs, *_ = self.apply_filters(qs, request)

            status_counts = qs.values('status').annotate(count=Count('id')).order_by('status')
            if not status_counts:
                status_counts = [
                    {'status': s, 'count': 0}
                    for s in ['pending', 'confirmed', 'delivered', 'cancelled', 'returned']
                ]

            serializer = StatusBreakdownSerializer(status_counts, many=True)
            return Response({'data': serializer.data})

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception("Error in StatusBreakdownView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderDateRangeAPIView(APIView):
    def get(self, request):
        try:
            min_max_dates = Orders.objects.aggregate(
                min_date=Min('delivery_date'),
                max_date=Max('delivery_date')
            )
            min_date = min_max_dates['min_date']
            max_date = min_max_dates['max_date']
            
            if min_date is None and max_date is None:
                return Response({
                    'min_order_date': None,
                    'max_order_date': None,
                    'message': 'No orders with delivery dates available.'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'min_order_date': min_date.isoformat() if min_date else None,
                'max_order_date': max_date.isoformat() if max_date else None
            })
        except Exception as exc:
            logger.exception("Error in OrderDateRangeAPIView")
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
