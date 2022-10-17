import csv
from django.core.management.base import BaseCommand, CommandError


from api.models import Company, Transaction


class Command(BaseCommand):
    help = 'Imports transactions and companies from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        try:
            csv_path = options['csv_path']
        except KeyError:
            raise CommandError('You must specify a CSV file path')

        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            t_size = 0
            c_size = 0
            transactions = []
            for row in csv_reader:
                try:
                    company_name = row[0].casefold()
                    company = Company.objects.get(name=company_name)
                except Company.DoesNotExist:
                    company = Company.objects.create(name=company_name)
                    c_size += 1
                transactions.append(
                    Transaction(
                        price=float(row[1]) / 100,
                        date=row[2],
                        status_transaction=row[3].casefold(),
                        status_approved=row[4].casefold() == 'true',
                        company=company,
                    )
                )
                t_size += 1
            Transaction.objects.bulk_create(transactions)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {t_size} transactions and {c_size} companies from CSV file')
        )
