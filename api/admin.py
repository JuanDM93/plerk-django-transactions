from django.contrib import admin

# Register your models here.
from .models import Company, Transaction


admin.site.register(Company)
admin.site.register(Transaction)
