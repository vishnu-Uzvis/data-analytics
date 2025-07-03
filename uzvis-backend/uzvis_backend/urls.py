from django.urls import path, include
from django.contrib import admin

admin.site.login = lambda request: admin.site.index(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analytics/', include('analytics.urls')),
]