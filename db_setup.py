import os
import django
from django.db import transaction

# 1. Django ortamını kuruyoruz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniedunote.settings')
django.setup()

from categories.models import University, Faculty, Department, Course


def run():
    print("🚀 Veri yükleme başladı (Hafıza Dostu Mod)...")

    target_unis = [
        "Anadolu Üniversitesi (Eskişehir)",
        "Atatürk Üniversitesi (Erzurum)",
        "İstanbul Üniversitesi",
        "Marmara Üniversitesi",
        "Sakarya Üniversitesi",
        "Bursa Uludağ Üniversitesi",
        "Selçuk Üniversitesi (Konya)",
        "Kocaeli Üniversitesi",
        "Gazi Üniversitesi (Ankara)",
        "Akdeniz Üniversitesi (Antalya)"
    ]

    fakulte_bolum_yapisi = {
        "Açık ve Uzaktan Öğretim Fakültesi": [
            "Çocuk Gelişimi", "Adalet", "Sosyal Hizmetler",
            "Tıbbi Dokümantasyon", "İlahiyat (Önlisans)",
            "Halkla İlişkiler", "İşletme Yönetimi"
        ],
        "Hukuk Fakültesi": ["Hukuk"],
        "İktisadi ve İdari Bilimler": ["İşletme", "İktisat", "Siyaset Bilimi", "Maliye"],
        "Eğitim Fakültesi": ["Sınıf Öğretmenliği", "Okul Öncesi Öğretmenliği", "Özel Eğitim"],
        "Fen-Edebiyat Fakültesi": ["Tarih", "Türk Dili ve Edebiyatı", "Psikoloji"],
        "Sağlık Bilimleri": ["Hemşirelik", "Ebelik"]
    }

    courses_sample = [
        "Atatürk İlkeleri ve İnkılap Tarihi",
        "Türk Dili I",
        "Yabancı Dil I (İngilizce)",
        "Temel Hukuk Bilgisi",
        "Genel Muhasebe",
        "İletişim Becerileri",
        "Giriş ve Algoritma",
        "İktisada Giriş"
    ]

    # Her üniversiteyi ayrı ayrı işleyip hafızayı rahatlatacağız
    for uni_name in target_unis:
        try:
            # transaction.atomic: İşlemleri paketleyip toplu yapar, RAM'i korur
            with transaction.atomic():
                uni, _ = University.objects.get_or_create(name=uni_name)

                for fakulte_adi, bolumler in fakulte_bolum_yapisi.items():
                    fac, _ = Faculty.objects.get_or_create(university=uni, name=fakulte_adi)

                    for bolum_adi in bolumler:
                        dept, _ = Department.objects.get_or_create(faculty=fac, name=bolum_adi)

                        # Dersleri toplu oluşturma listesi (Bulk Create Hazırlığı)
                        ders_listesi = []
                        for course_name in courses_sample:
                            # Önce var mı diye kontrol etmemiz lazım, yoksa bulk_create patlar
                            if not Course.objects.filter(department=dept, name=course_name).exists():
                                ders_listesi.append(Course(department=dept, name=course_name))

                        # Hepsini tek seferde veritabanına göm
                        if ders_listesi:
                            Course.objects.bulk_create(ders_listesi)

            print(f"✅ {uni_name} tamamlandı.")  # Sadece üniversite bitince yaz

        except Exception as e:
            print(f"❌ {uni_name} eklenirken hata: {str(e)}")

    print("🎉 MİSYON TAMAMLANDI! (RAM patlamadan hallettik)")


if __name__ == '__main__':
    run()