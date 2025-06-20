from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/analytics/', include('analytics.urls')),
    path('api-token-auth/', include('rest_framework.authtoken.urls')),
]