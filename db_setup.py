import os
import django
import time

# 1. Django ortamını kuruyoruz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniedunote.settings')
django.setup()

from categories.models import University, Faculty, Department, Course


def run():
    print("🚀 Veri yükleme başladı (SÜPER HAFİF MOD)...")

    # SADECE TEK BİR ÜNİVERSİTE (Test için)
    uni_name = "Anadolu Üniversitesi (Eskişehir)"

    fakulte_bolum_yapisi = {
        "Açık ve Uzaktan Öğretim Fakültesi": [
            "Çocuk Gelişimi", "Adalet", "İlahiyat (Önlisans)", "İşletme Yönetimi"
        ]
    }

    courses_sample = [
        "Atatürk İlkeleri ve İnkılap Tarihi",
        "Türk Dili I",
        "Yabancı Dil I (İngilizce)",
        "Temel Hukuk Bilgisi"
    ]

    try:
        # Üniversiteyi oluştur
        uni, created = University.objects.get_or_create(name=uni_name)
        print(f"✅ Üniversite işlendi: {uni_name}")

        for fakulte_adi, bolumler in fakulte_bolum_yapisi.items():
            fac, _ = Faculty.objects.get_or_create(university=uni, name=fakulte_adi)

            for bolum_adi in bolumler:
                dept, _ = Department.objects.get_or_create(faculty=fac, name=bolum_adi)

                # Dersleri tek tek, yavaş yavaş ekle (Hafıza şişmesin)
                for course_name in courses_sample:
                    Course.objects.get_or_create(department=dept, name=course_name)

        print("🎉 MİSYON TAMAMLANDI! (Bu sefer kesin)")

    except Exception as e:
        print(f"❌ Hata oldu: {str(e)}")


if __name__ == '__main__':
    run()