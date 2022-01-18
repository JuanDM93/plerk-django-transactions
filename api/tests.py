from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response

# Create your tests here.
from datetime import datetime
from pytz import UTC
from django.contrib.auth import get_user_model

from .models import Company, Transaction
from .serializers import CompanySerializer, TransactionSerializer, CompanySummarySerializer, SummarySerializer


User = get_user_model()


class ModelTests(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_company_creation(self):
        company = Company.objects.create(
            name='Test Company',
            status='active',
        )
        self.assertEqual(company.name, 'Test Company')
        self.assertEqual(company.status, 'active')

    def test_transaction_creation(self):
        now = datetime.now(tz=UTC)
        company = Company.objects.create(
            name='Test Company',
            status='active',
        )
        transaction = Transaction.objects.create(
            company_id=company,
            date=now,
            price=100,
            status_transaction='confirmed',
            status_approved=True,
            final_payment=True
        )
        self.assertEqual(transaction.company_id, company)
        self.assertEqual(transaction.date, now)
        self.assertEqual(transaction.price, 100)
        self.assertEqual(transaction.final_payment, True)


class SerializerTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_company_serializer(self):
        company = Company.objects.create(
            name='Test Company',
            status='active',
        )
        serializer = CompanySerializer(company)
        self.assertEqual(serializer.data['name'], 'Test Company')
        self.assertEqual(serializer.data['status'], 'active')

    def test_transaction_serializer(self):
        now = datetime.now(tz=UTC)
        company = Company.objects.create(
            name='Test Company',
            status='active',
        )
        transaction = Transaction.objects.create(
            company_id=company,
            date=now,
            price=100,
            status_transaction='confirmed',
            status_approved=True,
            final_payment=True
        )
        serializer = TransactionSerializer(transaction)
        self.assertEqual(serializer.data['final_payment'], True)
        self.assertEqual(serializer.data['company_id']['id'], company.id)


class SummaryTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_summary_serializer(self):
        now = datetime.now(tz=UTC)
        company = Company.objects.create(
            name='Test Company',
            status='active',
        )
        summary = SummarySerializer(
            data={
                'most_selling_company': CompanySerializer(company).data,
                'least_selling_company': CompanySerializer(company).data,
                'total_effective_revenue': 100,
                'total_canceled_revenue': 0,
                'most_canceled_company': CompanySerializer(company).data
            }
        )
        if summary.is_valid():
            return Response(summary.data, status=status.HTTP_200_OK)
        return Response(summary.errors, status=status.HTTP_400_BAD_REQUEST)

    def test_company_summary_serializer(self):
        now = datetime.now(tz=UTC)
        summary = CompanySummarySerializer(
            data={
                'name': 'Test Company',
                'total_effective_revenue': 100,
                'total_canceled_revenue': 0,
                'most_transaction_date': now
            }
        )
        if summary.is_valid():
            return Response(summary.data, status=status.HTTP_200_OK)
        return Response(summary.errors, status=status.HTTP_400_BAD_REQUEST)
