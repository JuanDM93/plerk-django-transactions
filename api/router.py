from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
    SummaryCompanyView,
    SummaryGlobalView,
)


urlpatterns = [
    path(
        'summary/<uuid:company_uuid>',
        SummaryCompanyView.as_view(),
        name='summary_company'
    ),
    path(
        'summary',
        SummaryGlobalView.as_view(),
        name='summary_global'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
