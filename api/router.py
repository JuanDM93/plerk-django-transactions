from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('summaries/', include('api.views.summary.urls')),
    path('companies/', include('api.views.company.urls')),
    path('transactions/', include('api.views.transaction.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
