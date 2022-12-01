from django.urls import path

from api.views.transaction.crud import (
    TransactionList,
    TransactionDetail,
)

urlpatterns = [
    path(
        '',
        TransactionList.as_view(),
        name='transaction_list'
    ),
    path(
        '<uuid:transaction_uuid>',
        TransactionDetail.as_view(),
        name='transaction_detail'
    ),
]
