from django.db import models
from abc import abstractmethod, ABC

from plerk.error_handling import ErrorCodes
from plerk.error_handling import CustomError


class CustomBaseManager(ABC, models.Manager):

    @property
    @abstractmethod
    def error(self):
        """abstract property, it is necessary to be
        implemented in the subclass according to the error that you want to Raise.
        Raises:
            NotImplementedError.
        """
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        """get an instance or raise plerk error.

        Raises:
            CustomError: instance not found.

        Returns:
            Instance: instance to get.
        """
        try:
            return super().get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise self.error


class CompanyManager(CustomBaseManager):
    error = CustomError(**ErrorCodes.COMPANY_NOT_FOUND.value)


class TransactionManager(CustomBaseManager):
    error = CustomError(**ErrorCodes.TRANSACTION_NOT_FOUND.value)
