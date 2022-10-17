from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

from .models import Transaction, Company
from .serializers import SummarySerializer, CompanySummarySerializer, CompanySerializer


class SummaryView(APIView):
    def get(self, request, format=None):
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
        try:
            total_effective_revenue = confirmed_transactions.aggregate(
                Sum('price')).get('price__sum')
            canceled_transactions = transactions.exclude(
                status_transaction='closed',
                status_approved=True
            )
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

        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyView(APIView):
    def get(self, request, pk, format=None):
        """
        Return a summary report of transactions for a specific company
            - name
            - total effective transactions
            - total canceled transactions
            - date with most transactions
        """
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(company_id=company.id,)
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
            'name': company.name.title(),
            'total_effective_transactions': effective_transactions.count(),
            'total_canceled_transactions': canceled_transactions.count(),
            'most_transactions_date': most_transaction_date,
        }
        serializer = CompanySummarySerializer(data=company_summary)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
