from django.db import models


COMPANY_STATUS_CHOICES = (
    ("active", "Active"),
    ("inactive", "Inactive"),
)

TRANSACTION_STATUS_CHOICES = (
    ("closed", "Closed"),
    ("reversed", "Reversed"),
    ("pending", "Pending"),

    ("funding", "Funding"),
    ("funding-user", "Funding User"),
)


class Company(models.Model):
    """
    - ID (en el formato que se considere más seguro)
    - Nombre
    - Status (activa/inactiva)
    """
    name = models.CharField(max_length=100)
    status = models.CharField(
        choices=COMPANY_STATUS_CHOICES,
        default='active',
        max_length=10
    )

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]


class Transaction(models.Model):
    """
    - ID (en el formato que se considere más seguro)
    - ID de empresa
    - Price (el price actual no viene en la cantidad real... requiere una conversión... 😉) o evaluación por ser costos reales
    - Fecha de transacción
    - Estatus de transacción
        - closed —> transaccion cobrada
        - reversed —> cobro realizado y regresado (para validar tarjeta)
        - pending —> pendiente de cobrar
    - Estatus de aprobación
        - false —> no se hizo un cobro
        - true —>  el cobro si fue aplicado a la tarjeta
    - Cobro Final  (Boolean)
        - Este punto es una combinación de "Estatus de transacción y estatus de aprobación"
            - Sólo se deben cobrar aquellas combinaciones que sean:
                - status_transaction = closed
                - status_approved = true
    """
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    status_transaction = models.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        default='pending',
        max_length=12
    )
    status_approved = models.BooleanField()
    final_payment = models.BooleanField()

    def __str__(self):
        return f'{self.company_id} - {self.price} - {self.date} - {self.status_transaction}'

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["date"]
