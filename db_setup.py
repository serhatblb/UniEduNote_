import os
import django

# 1. Django ortamını kuruyoruz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniedunote.settings')
django.setup()

# Senin YENİ ve SADE modellerini çağırıyoruz
from categories.models import University, Faculty, Department, Course


def run():
    print("🚀 Stratejik Veri Tabanı Doldurma Başladı (Yeni Modellerle)...")

    # --- 1. HEDEF KİTLE: EN KALABALIK ÜNİVERSİTELER ---
    target_unis = [
        "Anadolu Üniversitesi (Eskişehir)",  # Açıköğretim Kralı
        "Atatürk Üniversitesi (Erzurum)",  # ATA-AÖF
        "İstanbul Üniversitesi",  # AUZEF
        "Marmara Üniversitesi",
        "Sakarya Üniversitesi",
        "Bursa Uludağ Üniversitesi",
        "Selçuk Üniversitesi (Konya)",
        "Kocaeli Üniversitesi",
        "Gazi Üniversitesi (Ankara)",
        "Akdeniz Üniversitesi (Antalya)"
    ]

    # --- 2. BÖLÜM STRATEJİSİ (FAKÜLTE -> BÖLÜMLER) ---
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

    # --- 3. DERS ÖRNEKLERİ ---
    # ARTIK SADECE İSİM VAR (Code, Year vs. yok)
    courses_sample = [
        "Atatürk İlkeleri ve İnkılap Tarihi",
        "Türk Dili I",
        "Yabancı Dil I (İngilizce)",
        "Temel Hukuk Bilgisi",
        "Genel Muhasebe",
        "İletişim Becerileri",
        "Giriş ve Algoritma",
        "İktisada Giriş",
        "Anayasa Hukuku"
    ]

    for uni_name in target_unis:
        # Üniversite oluştur
        uni, created = University.objects.get_or_create(name=uni_name)
        if created:
            print(f"✅ Üniversite: {uni_name}")

        # Fakülteleri ve Bölümleri dönüyoruz
        for fakulte_adi, bolumler in fakulte_bolum_yapisi.items():

            # Eğer üniversite adında "Teknik" geçiyorsa ve fakülte "Hukuk" ise ekleme (saçma olmasın)
            # Ama senin liste genel olduğu için hepsini ekleyebiliriz, sorun yok.

            # Fakülte oluştur
            fac, _ = Faculty.objects.get_or_create(university=uni, name=fakulte_adi)

            for bolum_adi in bolumler:
                # Bölüm oluştur
                dept, _ = Department.objects.get_or_create(faculty=fac, name=bolum_adi)

                # Dersleri ekle (Sadece isim olarak)
                for course_name in courses_sample:
                    Course.objects.get_or_create(
                        department=dept,
                        name=course_name
                        # DİKKAT: code, class_year, term_season ARTIK YOK. Sildik.
                    )

    print("🎉 MİSYON TAMAMLANDI! Stratejik veriler hatasız yüklendi.")


if __name__ == '__main__':
    run()