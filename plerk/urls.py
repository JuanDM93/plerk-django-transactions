from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.permissions import AllowAny

from drf_yasg.openapi import Info, License
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    Info(
        title="Plerk-Backend API",
        default_version='v1',
        description="Technical Rest API test",
        license=License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

docs_patterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('api.router')),
    path('docs/', include(docs_patterns)),
]
