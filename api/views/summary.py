from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum, Count

from api.models import (
    Transaction,
    Company,
)
from api.serializers import (
    SummarySerializer,
    CompanySerializer,
)


class SummaryGlobalView(APIView):

    serializer_class = SummarySerializer

    def get(self, request):
        """
        Return a summary report of transactions
            - most selling company
            - least selling company
            - total revenue
            - total canceled revenue
            - most canceled company
        """
        transactions = Transaction.objects.all().select_related('company')
        confirmed_transactions = transactions.filter(
            status_transaction='closed',
            status_approved=True
        )
        canceled_transactions = transactions.exclude(
            status_transaction='closed',
            status_approved=True
        )
        try:
            total_effective_revenue = confirmed_transactions.aggregate(
                Sum('price')).get('price__sum')
            total_canceled_revenue = canceled_transactions.aggregate(
                Sum('price')).get('price__sum')

            sells = confirmed_transactions.values(
                'company').annotate(t_revenue=Sum('price'))

            most_selling_company = sells.order_by('-t_revenue')[0]
            most_selling_company = Company.objects.get(
                pk=most_selling_company['company'])

            least_selling_company = sells.order_by('t_revenue')[0]
            least_selling_company = Company.objects.get(
                pk=least_selling_company['company'])

            most_canceled_company = canceled_transactions.values('company').annotate(
                total_canceled=Count('company')).order_by('-total_canceled')[0]
            most_canceled_company = Company.objects.get(
                pk=most_canceled_company['company'])
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        summary = SummarySerializer(
            data={
                'most_selling_company': CompanySerializer(most_selling_company).data,
                'least_selling_company': CompanySerializer(least_selling_company).data,
                'total_effective_revenue': total_effective_revenue / 100,
                'total_canceled_revenue': total_canceled_revenue / 100,
                'most_canceled_company': CompanySerializer(most_canceled_company).data,
            }
        )
        if summary.is_valid():
            return Response(summary.data, status=status.HTTP_200_OK)
        return Response(summary.errors, status=status.HTTP_400_BAD_REQUEST)
