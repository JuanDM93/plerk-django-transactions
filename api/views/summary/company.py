from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count
from django.db.models.functions import TruncDate

from api.models import (
    Transaction,
    Company,
)
from api.serializers import (
    SummaryCompanySerializer,
    CompanySerializer,
)
from plerk.error_handling import (
    CustomError,
    ErrorCodes,
)


class SummaryCompanyView(APIView):

    serializer_class = SummaryCompanySerializer

    def get(self, request, company_uuid):
        """
        Return a summary report of transactions for a specific company
            - name
            - total effective transactions
            - total canceled transactions
            - date with most transactions
        """
        company = Company.objects.get(uuid=company_uuid)
        transactions = Transaction.objects.filter(company_id=company.id)
        if not transactions:
            raise CustomError(**ErrorCodes.NO_TRANSACTIONS_FOUND.value)
        effective_transactions = transactions.filter(
            status_transaction='closed',
            status_approved=True,
        )
        canceled_transactions = transactions.exclude(
            status_transaction='closed',
            status_approved=True,
        )
        most_transaction_date = transactions.values('date').annotate(
            r_date=TruncDate('date')).values('r_date').annotate(
            c_date=Count('r_date')
        ).order_by('-c_date')[0].get('r_date')

        company_summary = {
            'company': CompanySerializer(company).data,
            'total_effective_transactions': effective_transactions.count(),
            'total_canceled_transactions': canceled_transactions.count(),
            'most_transactions_date': most_transaction_date,
        }
        serializer = SummaryCompanySerializer(data=company_summary)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
