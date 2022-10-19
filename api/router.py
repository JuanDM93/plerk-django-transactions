from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
    CompanyView,
    SummaryView,
)


urlpatterns = [
    path(
        'summary/',
        SummaryView.as_view(),
        name='summary'
    ),
    path(
        'companies/<uuid:company_uuid4>/',
        CompanyView.as_view(),
        name='companies'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
