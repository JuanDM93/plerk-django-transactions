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
            for row in csv_reader:
                try:
                    company_name = row[0].casefold()
                    company = Company.objects.get(name=company_name)
                except Company.DoesNotExist:
                    company = Company.objects.create(name=company_name)
                Transaction.objects.create(
                    price=float(row[1]) / 100,
                    date=row[2],
                    status_transaction=row[3],
                    status_approved=bool(row[4].capitalize()),
                    company_id=company,
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully imported transactions and companies from CSV file'))
