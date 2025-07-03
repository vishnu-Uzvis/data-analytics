from django.urls import path
from . import views

urlpatterns = [
    path('kpis/', views.KpisView.as_view(), name='kpis'),
    path('order-count/', views.OrderCountView.as_view(), name='order_count'),
    path('revenue/', views.RevenueView.as_view(), name='revenue'),
    path('revenue-details/', views.RevenueDetailView.as_view(), name='revenue_details'),  # Added for overall revenue module
    path('payment-methods/', views.PaymentMethodsView.as_view(), name='payment_methods'),
    path('status-breakdown/', views.StatusBreakdownView.as_view(), name='status_breakdown'),
    path('order-date-range/', views.OrderDateRangeAPIView.as_view(), name='order_date_range'),
]
