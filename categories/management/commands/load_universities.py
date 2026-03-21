import os
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from categories.models import University, Faculty, Department


class Command(BaseCommand):
    help = 'SQL dosyalarından üniversite, fakülte ve bölümleri hızlıca yükler'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Mevcut verileri silip yeniden yükle',
        )

    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'universite-fakulte-bolum-listesi')

        if options['clear']:
            self.stdout.write('Mevcut veriler siliniyor...')
            Department.objects.all().delete()
            Faculty.objects.all().delete()
            University.objects.all().delete()
            self.stdout.write(self.style.WARNING('Silindi.'))

        if University.objects.exists() and not options['clear']:
            self.stdout.write(self.style.WARNING(
                f'Veritabanında zaten {University.objects.count()} üniversite var. '
                'Yeniden yüklemek için --clear kullanın.'
            ))
            return

        uni_file = os.path.join(base_path, 'universite.sql')
        fac_file = os.path.join(base_path, 'universite_fakulte.sql')
        dep_file = os.path.join(base_path, 'universite_bolum.sql')

        # ── 1. ÜNİVERSİTELER ──
        self.stdout.write('Üniversiteler yükleniyor...')
        uni_rows = self._parse_sql(uni_file, r'\((\d+),\s*\'((?:[^\'\\]|\\.)*)\',\s*\d+\)')
        # uni_rows: [(sql_id, name), ...]

        uni_objects = [University(name=name) for _, name in uni_rows]
        with transaction.atomic():
            created_unis = University.objects.bulk_create(uni_objects)

        # sql_id → Django pk mapping
        sql_to_uni = {int(uni_rows[i][0]): created_unis[i].pk for i in range(len(created_unis))}
        self.stdout.write(self.style.SUCCESS(f'  {len(created_unis)} üniversite yüklendi.'))

        # ── 2. FAKÜLTELER ──
        self.stdout.write('Fakülteler yükleniyor...')
        # Pattern: (fakulte_id, name, universite_id, status)
        fac_rows = self._parse_sql(fac_file, r'\((\d+),\s*\'((?:[^\'\\]|\\.)*)\',\s*(\d+),\s*\d+\)')
        # fac_rows: [(fak_id, name, uni_sql_id), ...]

        fac_data = []
        for fak_id, name, uni_sql_id in fac_rows:
            uni_pk = sql_to_uni.get(int(uni_sql_id))
            if uni_pk:
                fac_data.append((int(fak_id), Faculty(university_id=uni_pk, name=name)))

        fac_sql_ids = [d[0] for d in fac_data]
        fac_objects = [d[1] for d in fac_data]

        created_facs = []
        BATCH = 500
        with transaction.atomic():
            for i in range(0, len(fac_objects), BATCH):
                batch = Faculty.objects.bulk_create(fac_objects[i:i + BATCH])
                created_facs.extend(batch)

        sql_to_fac = {fac_sql_ids[i]: created_facs[i].pk for i in range(len(created_facs))}
        self.stdout.write(self.style.SUCCESS(f'  {len(created_facs)} fakülte yüklendi.'))

        # ── 3. BÖLÜMLER ──
        self.stdout.write('Bölümler yükleniyor... (21K+ kayıt, biraz sürebilir)')
        # Pattern: (bolum_id, sure, tip, fakulte_id, universite_id, name, status)
        dep_rows = self._parse_sql(
            dep_file,
            r'\(\d+,\s*\d+,\s*\'[^\']*\',\s*(\d+),\s*\d+,\s*\'((?:[^\'\\]|\\.)*)\',\s*\d+\)'
        )
        # dep_rows: [(fak_sql_id, name), ...]

        dep_objects = []
        for fak_sql_id, name in dep_rows:
            fac_pk = sql_to_fac.get(int(fak_sql_id))
            if fac_pk:
                dep_objects.append(Department(faculty_id=fac_pk, name=name))

        total = 0
        with transaction.atomic():
            for i in range(0, len(dep_objects), BATCH):
                batch = Department.objects.bulk_create(dep_objects[i:i + BATCH])
                total += len(batch)
                if total % 5000 == 0 or total == len(dep_objects):
                    self.stdout.write(f'  {total}/{len(dep_objects)} bölüm işlendi...')

        self.stdout.write(self.style.SUCCESS(f'  {total} bölüm yüklendi.'))
        self.stdout.write(self.style.SUCCESS(
            f'\nTamamlandı! {len(created_unis)} üniversite, '
            f'{len(created_facs)} fakülte, {total} bölüm yüklendi.'
        ))

    def _parse_sql(self, filepath, pattern):
        with open(filepath, encoding='utf-8', errors='replace') as f:
            content = f.read()
        return re.findall(pattern, content)
