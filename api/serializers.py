from rest_framework import serializers
from api.models import Transaction, Company


class CompanySerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Company
        fields = ('name', 'status')


class TransactionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    status_transaction = serializers.CharField(
        source='get_status_transaction_display')

    class Meta:
        model = Transaction
        fields = (
            'date',
            'company',
            'price',
            'status_transaction',
        )

    def get_price(self, obj):
        return obj.price / 100


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
    total_effective_transactions = serializers.IntegerField()
    total_canceled_transactions = serializers.IntegerField()
    most_transactions_date = serializers.DateField()
