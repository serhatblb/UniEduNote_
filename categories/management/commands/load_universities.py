from django.core.management.base import BaseCommand
from categories.models import University, Faculty, Department
import pandas as pd

class Command(BaseCommand):
    help = "Excel dosyasındaki üniversite, fakülte ve bölümleri veritabanına yükler."

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str, help='Excel dosyasının yolu')

    def handle(self, *args, **options):
        path = options['excel_path']
        xls = pd.ExcelFile(path)

        # 1. Üniversiteler
        universities = pd.read_excel(xls, sheet_name='Universiteler')
        for _, row in universities.iterrows():
            University.objects.get_or_create(name=row['university_name'])

        # 2. Fakülteler
        faculties = pd.read_excel(xls, sheet_name='Fakulteler')
        for _, row in faculties.iterrows():
            uni = University.objects.filter(name=row['university_name']).first()
            if uni:
                Faculty.objects.get_or_create(name=row['faculty_name'], university=uni)

        # 3. Bölümler
        departments = pd.read_excel(xls, sheet_name='Bolumler')
        for _, row in departments.iterrows():
            fac = Faculty.objects.filter(name=row['faculty_name']).first()
            if fac:
                Department.objects.get_or_create(name=row['department_name'], faculty=fac)

        self.stdout.write(self.style.SUCCESS("Excel verileri başarıyla yüklendi."))
