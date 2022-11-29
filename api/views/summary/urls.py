from django.urls import path

from api.views.summary import (
    SummaryCompanyView,
    SummaryGlobalView,
)


urlpatterns = [
    path(
        '',
        SummaryGlobalView.as_view(),
        name='summary_global'
    ),
    path(
        '<uuid:company_uuid>',
        SummaryCompanyView.as_view(),
        name='summary_company'
    ),
]
