from rest_framework import serializers

from api.models import (
    Transaction,
    Company,
)


class CompanySerializer(serializers.ModelSerializer):
    status = serializers.CharField(
        source='get_status_display',
        required=False,
    )

    class Meta:
        model = Company
        fields = (
            'uuid',
            'name',
            'status',
        )


class TransactionSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Company.objects.all(),
    )
    status_transaction = serializers.CharField(
        source='get_status_transaction_display',
        required=False,
    )

    class Meta:
        model = Transaction
        fields = (
            'uuid',
            'date',
            'company',
            'price',
            'status_transaction',
            'status_approved',
        )

    def get_price(self, obj):
        return obj.price / 100
