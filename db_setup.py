import os
import django

# 1. Django ortamını kuruyoruz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniedunote.settings')
django.setup()

# Modellerini çağırıyoruz (senin app ismine göre categories veya academic)
from categories.models import University, Faculty, Department, Course


def run():
    print("🚀 Stratejik Veri Tabanı Doldurma Başladı (Hedef Kitle Odaklı)...")

    # --- 1. HEDEF KİTLE: EN KALABALIK ÜNİVERSİTELER ---
    target_unis = [
        "Anadolu Üniversitesi (Eskişehir)",  # Açıköğretim Kralı
        "Atatürk Üniversitesi (Erzurum)",  # ATA-AÖF çok popüler
        "İstanbul Üniversitesi",  # AUZEF + Kalabalık kampüs
        "Marmara Üniversitesi",  # Çok öğrencisi var
        "Sakarya Üniversitesi",  # Öğrenci şehri resmen
        "Bursa Uludağ Üniversitesi",
        "Selçuk Üniversitesi (Konya)",
        "Kocaeli Üniversitesi",
        "Gazi Üniversitesi (Ankara)",
        "Akdeniz Üniversitesi (Antalya)"
    ]

    # --- 2. BÖLÜM STRATEJİSİ ---
    # Not arama ihtimali en yüksek bölümler (Sözel ağırlıklı, ezber gerektiren)

    # A) Açıköğretim ve Önlisans Favorileri (Anadolu, Atatürk, İstanbul için)
    acikogretim_bolumleri = [
        "Çocuk Gelişimi",
        "Adalet",
        "Sosyal Hizmetler",
        "Tıbbi Dokümantasyon ve Sekreterlik",
        "İlahiyat (Önlisans)",
        "Halkla İlişkiler ve Tanıtım",
        "İşletme Yönetimi"
    ]

    # B) Kampüs Bölümleri (Vize/Finalde not arayanlar)
    kampus_fakulteleri = {
        "Hukuk Fakültesi": ["Hukuk"],
        "İktisadi ve İdari Bilimler": ["İşletme", "İktisat", "Siyaset Bilimi ve Kamu Yönetimi", "Maliye"],
        "Eğitim Fakültesi": ["Sınıf Öğretmenliği", "Okul Öncesi Öğretmenliği", "Özel Eğitim Öğretmenliği"],
        "İlahiyat Fakültesi": ["İlahiyat"],
        "Fen-Edebiyat Fakültesi": ["Tarih", "Türk Dili ve Edebiyatı", "Psikoloji"],
        "Sağlık Bilimleri": ["Hemşirelik", "Ebelik"]
    }

    # --- 3. DERS ÖRNEKLERİ (GENEL) ---
    courses_sample = [
        {"name": "Atatürk İlkeleri ve İnkılap Tarihi", "code": "TAR101", "year": 1, "term": "Guz"},
        {"name": "Türk Dili I", "code": "TUR101", "year": 1, "term": "Guz"},
        {"name": "Yabancı Dil I (İngilizce)", "code": "ING101", "year": 1, "term": "Guz"},
        {"name": "Temel Hukuk Bilgisi", "code": "HUK101", "year": 1, "term": "Bahar"},
        {"name": "Genel Muhasebe", "code": "ISL201", "year": 2, "term": "Guz"},
        {"name": "İletişim Becerileri", "code": "ILT105", "year": 1, "term": "Bahar"},
    ]

    for uni_name in target_unis:
        uni, created = University.objects.get_or_create(name=uni_name)
        if created:
            print(f"✅ Üniversite: {uni_name}")

        # Eğer Açıköğretim devi ise, o fakülteyi özel ekle
        if "Anadolu" in uni_name or "Atatürk" in uni_name or "İstanbul" in uni_name:
            aof_fakulte, _ = Faculty.objects.get_or_create(university=uni, name="Açık ve Uzaktan Öğretim Fakültesi")
            for bolum in acikogretim_bolumleri:
                dept, _ = Department.objects.get_or_create(faculty=aof_fakulte, name=bolum)
                # Örnek dersleri bas
                for course in courses_sample:
                    Course.objects.get_or_create(
                        department=dept,
                        name=course['name'],
                        code=course['code'],
                        defaults={'class_year': course['year'], 'term_season': course['term']}
                    )

        # Diğer standart fakülteleri herkese ekle
        for fakulte_adi, bolumler in kampus_fakulteleri.items():
            fac, _ = Faculty.objects.get_or_create(university=uni, name=fakulte_adi)
            for bolum_adi in bolumler:
                dept, _ = Department.objects.get_or_create(faculty=fac, name=bolum_adi)
                # Dersleri ekle
                for course in courses_sample:
                    Course.objects.get_or_create(
                        department=dept,
                        name=course['name'],
                        code=course['code'],
                        defaults={'class_year': course['year'], 'term_season': course['term']}
                    )

    print("🎉 MİSYON TAMAMLANDI! En çok not aranan bölümler yüklendi.")


if __name__ == '__main__':
    run()