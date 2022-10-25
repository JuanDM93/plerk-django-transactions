from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from plerk.settings import DEBUG

from plerk.error_handling import CustomError

from logging import getLogger


def custom_exception_handler(exc, context):
    """ Exception Handler """

    response = exception_handler(exc, context)
    if response:
        return response

    if isinstance(exc, CustomError):
        return Response({
            'detail': exc.message,
            'error_code': int(exc.error_code),
        }, status=exc.status_code)

    if DEBUG:
        logger = getLogger(__name__)
        logger.error(str(exc))
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    # sentry_sdk.set_context('Context', context)
    return Response(
        {'detail': 'Internal Server Error'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
