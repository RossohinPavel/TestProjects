from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.api.v1.views import LogViewSet

v1_router = DefaultRouter()
v1_router.register('logs', LogViewSet, basename='logs')


urlpatterns = [
    path("", include(v1_router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'), 
]
