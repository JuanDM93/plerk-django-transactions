from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from api.models import Transaction
from api.serializers import TransactionSerializer


class TransactionList(APIView):
    """
    List all transactions, or create a new transaction.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDetail(APIView):
    """
    Retrieve, update or delete a transaction instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, transaction_uuid):
        return Transaction.objects.get(uuid=transaction_uuid)

    def get(self, request, transaction_uuid, format=None):
        transaction = self.get_object(transaction_uuid)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, transaction_uuid, format=None):
        transaction = self.get_object(transaction_uuid)
        serializer = TransactionSerializer(transaction, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, transaction_uuid, format=None):
        transaction = self.get_object(transaction_uuid)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
