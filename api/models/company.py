from uuid import uuid4
from django.db import models

from api.models.managers import CompanyManager


class Company(models.Model):
    """
    - ID (en el formato que se considere más seguro)
    - Nombre
    - Status (activa/inactiva)
    """

    objects = CompanyManager()

    COMPANY_STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    uuid = models.UUIDField(editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=100)
    status = models.CharField(
        choices=COMPANY_STATUS_CHOICES,
        default='active',
        max_length=10
    )

    def __str__(self):
        return f"{self.name.title()} - {self.get_status_display()}"

    def get_status_display(self):
        return dict(self.COMPANY_STATUS_CHOICES)[self.status]

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]
