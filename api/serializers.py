from rest_framework import serializers
from .models import Transaction, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'status')


class TransactionSerializer(serializers.ModelSerializer):
    company_id = CompanySerializer()

    class Meta:
        model = Transaction
        fields = (
            'id', 'company_id', 'price',
            'status_transaction', 'date',
            'status_approved',
        )


class SummarySerializer(serializers.Serializer):
    most_selling_company = CompanySerializer()
    least_selling_company = CompanySerializer()
    total_effective_revenue = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    total_canceled_revenue = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    most_canceled_company = CompanySerializer()


class CompanySummarySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total_effective_revenue = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    total_canceled_revenue = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    most_transaction_date = serializers.DateTimeField()
