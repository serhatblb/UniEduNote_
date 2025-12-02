from django.core.management.base import BaseCommand
from academic.models import University, Faculty, Department, Course


class Command(BaseCommand):
    help = 'Veritabanına başlangıç verilerini yükler (Top 10 Üni + Müfredat)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Veri yükleme işlemi başlıyor...")

        # Türkiye'nin En Kalabalık/Popüler 10 Üniversitesi
        data = [
            {
                "name": "İstanbul Teknik Üniversitesi",
                "faculties": [
                    {"name": "Bilgisayar ve Bilişim Fakültesi",
                     "depts": ["Bilgisayar Mühendisliği", "Yapay Zeka Mühendisliği"]},
                    {"name": "Elektrik-Elektronik Fakültesi",
                     "depts": ["Elektrik Mühendisliği", "Elektronik Haberleşme Müh."]},
                    {"name": "Mimarlık Fakültesi", "depts": ["Mimarlık", "Endüstriyel Tasarım"]}
                ]
            },
            {
                "name": "Yıldız Teknik Üniversitesi",
                "faculties": [
                    {"name": "Elektrik-Elektronik Fakültesi",
                     "depts": ["Bilgisayar Mühendisliği", "Elektrik Mühendisliği"]},
                    {"name": "Makine Fakültesi", "depts": ["Makine Mühendisliği", "Mekatronik Mühendisliği"]}
                ]
            },
            {
                "name": "ODTÜ",
                "faculties": [
                    {"name": "Mühendislik Fakültesi",
                     "depts": ["Bilgisayar Mühendisliği", "Havacılık ve Uzay Müh.", "Endüstri Mühendisliği"]},
                    {"name": "Fen Edebiyat Fakültesi", "depts": ["Psikoloji", "Fizik"]}
                ]
            },
            {
                "name": "İstanbul Üniversitesi",
                "faculties": [
                    {"name": "Hukuk Fakültesi", "depts": ["Hukuk"]},
                    {"name": "Siyasal Bilgiler Fakültesi", "depts": ["Siyaset Bilimi ve Kamu Yönetimi", "İşletme"]}
                ]
            },
            {
                "name": "Marmara Üniversitesi",
                "faculties": [
                    {"name": "Teknoloji Fakültesi", "depts": ["Bilgisayar Mühendisliği", "Makine Mühendisliği"]},
                    {"name": "İletişim Fakültesi", "depts": ["Radyo, Televizyon ve Sinema", "Halkla İlişkiler"]}
                ]
            },
            # Diğer üniversiteleri buraya aynı formatta ekleyebilirsin...
        ]

        # Her bölümde olması gereken ortak 1. sınıf dersleri
        common_courses_guz = [
            {"name": "Matematik I", "code": "MAT101"},
            {"name": "Fizik I", "code": "FIZ101"},
            {"name": "Türk Dili I", "code": "TUR101"},
            {"name": "İngilizce I", "code": "ING101"},
        ]

        common_courses_bahar = [
            {"name": "Matematik II", "code": "MAT102"},
            {"name": "Fizik II", "code": "FIZ102"},
            {"name": "Lineer Cebir", "code": "MAT104"},
        ]

        for uni_data in data:
            uni, created = University.objects.get_or_create(name=uni_data['name'])
            if created:
                self.stdout.write(f"✅ Üniversite eklendi: {uni.name}")

            for fac_data in uni_data['faculties']:
                faculty, _ = Faculty.objects.get_or_create(university=uni, name=fac_data['name'])

                for dept_name in fac_data['depts']:
                    dept, _ = Department.objects.get_or_create(faculty=faculty, name=dept_name)

                    # Dersleri Ekle (Sadece bu bölüm için)
                    # Güz Dönemi Dersleri
                    for course in common_courses_guz:
                        Course.objects.get_or_create(
                            department=dept,
                            name=course['name'],
                            code=course['code'],
                            class_year=1,
                            term_season='Guz'
                        )

                    # Bahar Dönemi Dersleri
                    for course in common_courses_bahar:
                        Course.objects.get_or_create(
                            department=dept,
                            name=course['name'],
                            code=course['code'],
                            class_year=1,
                            term_season='Bahar'
                        )

        self.stdout.write(self.style.SUCCESS('TÜM VERİLER BAŞARIYLA YÜKLENDİ! 🚀'))