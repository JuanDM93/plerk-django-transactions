from django.contrib import admin

# Register your models here.
from api.models import (
    Company,
    Transaction,
)


admin.site.register(Company)
admin.site.register(Transaction)
