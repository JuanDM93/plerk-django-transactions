from enum import Enum
from rest_framework import status


class ErrorCodes(Enum):
    # General
    UNKNOWN = {
        'error_code': 5000,
        'message': 'Unknown error',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    # Company
    COMPANY_NOT_FOUND = {
        'error_code': 1001,
        'message': 'Company not found',
        'status_code': status.HTTP_404_NOT_FOUND,
    }
    COMPANY_ALREADY_EXISTS = {
        'error_code': 1002,
        'message': 'Company already exists',
        'status_code': status.HTTP_400_BAD_REQUEST,
    }
    # Transaction
    TRANSACTION_NOT_FOUND = {
        'error_code': 2001,
        'message': 'Transaction not found',
        'status_code': status.HTTP_404_NOT_FOUND,
    }
    TRANSACTION_ALREADY_EXISTS = {
        'error_code': 2002,
        'message': 'Transaction already exists',
        'status_code': status.HTTP_400_BAD_REQUEST,
    }
    # Summary
    SUMMARY_NOT_FOUND = {
        'error_code': 3001,
        'message': 'Summary not found',
        'status_code': status.HTTP_404_NOT_FOUND,
    }
