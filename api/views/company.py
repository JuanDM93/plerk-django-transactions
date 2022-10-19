from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count
from django.db.models.functions import TruncDate

from api.models import (
    Transaction,
    Company,
)
from api.serializers import CompanySummarySerializer


class CompanyView(APIView):

    serializer_class = CompanySummarySerializer

    def get(self, request, company_uuid4):
        """
        Return a summary report of transactions for a specific company
            - name
            - total effective transactions
            - total canceled transactions
            - date with most transactions
        """
        # company_uuid4 = request.GET.get('uuid4')
        company = self.get_company(company_uuid4)
        transactions = Transaction.objects.filter(company_id=company.id,)
        effective_transactions = transactions.filter(
            status_transaction='closed',
            status_approved=True,
        )
        canceled_transactions = transactions.exclude(
            status_transaction='closed',
            status_approved=True,
        )
        try:
            most_transaction_date = transactions.values('date').annotate(
                r_date=TruncDate('date')).values('r_date').annotate(
                c_date=Count('r_date')
            ).order_by('-c_date')[0].get('r_date')

            company_summary = {
                'name': company.name.title(),
                'total_effective_transactions': effective_transactions.count(),
                'total_canceled_transactions': canceled_transactions.count(),
                'most_transactions_date': most_transaction_date,
            }
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = CompanySummarySerializer(data=company_summary)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_company(self, company_uuid):
        try:
            company = Company.objects.get(uuid=company_uuid)
        except Company.DoesNotExist:
            return Response(
                f'Company does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        return company
