from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum


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
        try:
            confirmed = Transaction.objects.filter(final_payment=True)
            total_revenue = confirmed.aggregate(Sum('price'))['price__sum']

            canceled = Transaction.objects.filter(final_payment=False)
            total_canceled = canceled.aggregate(Sum('price'))['price__sum']

            most_selling_company = confirmed.values('company_id').annotate(
                total_revenue=Sum('price')).order_by('-total_revenue')[0]
            most_selling_company = Company.objects.get(
                id=most_selling_company['company_id'])

            least_selling_company = confirmed.values('company_id').annotate(
                total_revenue=Sum('price')).order_by('total_revenue')[0]
            least_selling_company = Company.objects.get(
                id=least_selling_company['company_id'])

            most_canceled_company = canceled.values('company_id').annotate(
                cancels=Count('id')).order_by('-cancels')[0]
            most_canceled_company = Company.objects.get(
                id=most_canceled_company['company_id'])
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        summary = SummarySerializer(
            data={
                'most_selling_company': CompanySerializer(most_selling_company).data,
                'least_selling_company': CompanySerializer(least_selling_company).data,
                'total_effective_revenue': total_revenue,
                'total_canceled_revenue': total_canceled,
                'most_canceled_company': CompanySerializer(most_canceled_company).data
            }
        )
        if summary.is_valid():
            return Response(summary.data, status=status.HTTP_200_OK)
        return Response(summary.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyView(APIView):
    def get(self, request, pk, format=None):
        """
        Return a summary report of transactions for a specific company
            - name
            - total effective revenue
            - total canceled revenue
            - most transactions date
        """
        try:
            transactions = Transaction.objects.filter(company_id=pk)
            effective_transactions = transactions.filter(final_payment=True)
            canceled_transactions = transactions.filter(final_payment=False)

            total_effective_revenue = effective_transactions.aggregate(
                Sum('price'))['price__sum']
            total_canceled_revenue = canceled_transactions.aggregate(
                Sum('price'))['price__sum']

            most_transaction_date = transactions.annotate(
                dcount=Count('date')).order_by('-dcount')[0].date

            company_summary = {
                'name': Company.objects.get(id=pk).name,
                'total_effective_revenue': 0 if total_effective_revenue is None else total_effective_revenue,
                'total_canceled_revenue': 0 if total_canceled_revenue is None else total_canceled_revenue,
                'most_transaction_date': most_transaction_date,
            }
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySummarySerializer(data=company_summary)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
