from django.urls import path

from api.views.company.crud import (
    CompanyList,
    CompanyDetail,
)

urlpatterns = [
    path(
        '',
        CompanyList.as_view(),
        name='company_list'
    ),
    path(
        '<uuid:company_uuid>',
        CompanyDetail.as_view(),
        name='company_detail'
    ),
]
