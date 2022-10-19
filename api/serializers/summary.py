from rest_framework import serializers

from api.serializers.entities import CompanySerializer


class SummarySerializer(serializers.Serializer):
    most_selling_company = CompanySerializer()
    least_selling_company = CompanySerializer()
    total_effective_revenue = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    total_canceled_revenue = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    most_canceled_company = CompanySerializer()


class CompanySummarySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total_effective_transactions = serializers.IntegerField()
    total_canceled_transactions = serializers.IntegerField()
    most_transactions_date = serializers.DateField()
