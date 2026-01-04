"""
30 Üniversite Verisi Yükleme Scripti
Türkiye'de en çok tercih edilen üniversiteler için akademik hiyerarşi verisi
"""
import os
import django
import sys

# Django ortamını kur
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniedunote.settings')
django.setup()

from categories.models import University, Faculty, Department, Course

# 30 Üniversite ve Yapıları
UNIVERSITIES_DATA = {
    "İstanbul Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama Dilleri", "Veri Yapıları", "Algoritma Analizi", 
                "Yazılım Mühendisliği", "Veritabanı Sistemleri", "Web Programlama"
            ],
            "Elektrik-Elektronik Mühendisliği": [
                "Devre Analizi", "Sinyaller ve Sistemler", "Elektromanyetik Teori",
                "Mikroişlemciler", "Dijital Sistemler"
            ],
            "Endüstri Mühendisliği": [
                "Yöneylem Araştırması", "Üretim Planlama", "Kalite Kontrol",
                "İşletme Yönetimi"
            ]
        },
        "İktisat Fakültesi": {
            "İktisat": [
                "Mikroekonomi", "Makroekonomi", "Ekonometri", "Para Teorisi",
                "Uluslararası İktisat"
            ],
            "İşletme": [
                "Muhasebe", "Finansal Yönetim", "Pazarlama", "İnsan Kaynakları",
                "Stratejik Yönetim"
            ]
        },
        "Edebiyat Fakültesi": {
            "Türk Dili ve Edebiyatı": [
                "Eski Türk Edebiyatı", "Yeni Türk Edebiyatı", "Türk Halk Edebiyatı",
                "Dil Bilgisi"
            ],
            "Tarih": [
                "Osmanlı Tarihi", "Türkiye Cumhuriyeti Tarihi", "Ortaçağ Tarihi"
            ]
        }
    },
    "Ankara Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Nesne Yönelimli Programlama", "Bilgisayar Ağları", "Yapay Zeka",
                "Görüntü İşleme", "Güvenlik"
            ],
            "Makine Mühendisliği": [
                "Termodinamik", "Akışkanlar Mekaniği", "Makine Elemanları",
                "Isı Transferi"
            ]
        },
        "Hukuk Fakültesi": {
            "Hukuk": [
                "Anayasa Hukuku", "Medeni Hukuk", "Ceza Hukuku", "Ticaret Hukuku",
                "İdare Hukuku"
            ]
        }
    },
    "Boğaziçi Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Algoritmalar", "Bilgisayar Sistemleri", "Yazılım Geliştirme",
                "Makine Öğrenmesi", "Bilgisayar Grafikleri"
            ],
            "Endüstri Mühendisliği": [
                "Optimizasyon", "Simülasyon", "Tedarik Zinciri Yönetimi"
            ]
        },
        "İktisadi ve İdari Bilimler Fakültesi": {
            "İşletme": [
                "Yönetim Bilimi", "Pazarlama Stratejileri", "Finans",
                "Girişimcilik"
            ]
        }
    },
    "Orta Doğu Teknik Üniversitesi (ODTÜ)": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Veri Yapıları ve Algoritmalar", "İşletim Sistemleri",
                "Bilgisayar Ağları", "Yazılım Mühendisliği"
            ],
            "Elektrik-Elektronik Mühendisliği": [
                "Elektrik Devreleri", "Elektronik", "Haberleşme Sistemleri"
            ]
        }
    },
    "Hacettepe Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Veri Yapıları", "Algoritma", "Yazılım Mühendisliği"
            ]
        },
        "Tıp Fakültesi": {
            "Tıp": [
                "Anatomi", "Fizyoloji", "Biyokimya", "Patoloji", "Farmakoloji"
            ]
        }
    },
    "İstanbul Teknik Üniversitesi (İTÜ)": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Algoritma", "Veri Yapıları", "Yazılım Mühendisliği"
            ],
            "Elektrik Mühendisliği": [
                "Elektrik Devreleri", "Elektromanyetik", "Güç Sistemleri"
            ]
        }
    },
    "Anadolu Üniversitesi (AÖF)": {
        "Açık ve Uzaktan Öğretim Fakültesi": {
            "İşletme": [
                "Genel İşletme", "Muhasebe", "Pazarlama", "İnsan Kaynakları",
                "Yönetim ve Organizasyon"
            ],
            "İktisat": [
                "Mikroekonomi", "Makroekonomi", "Para-Banka", "Uluslararası İktisat"
            ],
            "Çocuk Gelişimi": [
                "Çocuk Gelişimi", "Erken Çocukluk Eğitimi", "Özel Eğitim"
            ],
            "Adalet": [
                "Hukukun Temel Kavramları", "Medeni Hukuk", "Ceza Hukuku",
                "İdare Hukuku"
            ]
        }
    },
    "Marmara Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Veri Yapıları", "Yazılım Mühendisliği"
            ]
        },
        "İktisat Fakültesi": {
            "İktisat": [
                "Mikroekonomi", "Makroekonomi", "Ekonometri"
            ]
        }
    },
    "Ege Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Algoritma", "Veri Yapıları"
            ]
        }
    },
    "Dokuz Eylül Üniversitesi": {
        "Mühendislik Fakültesi": {
            "Bilgisayar Mühendisliği": [
                "Programlama", "Yazılım Mühendisliği", "Veri Yapıları"
            ]
        }
    }
}

# Kalan 20 üniversite için basit yapı
ADDITIONAL_UNIVERSITIES = [
    "Gazi Üniversitesi", "Yıldız Teknik Üniversitesi", "Galatasaray Üniversitesi",
    "Koç Üniversitesi", "Sabancı Üniversitesi", "Bilkent Üniversitesi",
    "Uludağ Üniversitesi", "Akdeniz Üniversitesi", "Çukurova Üniversitesi",
    "Karadeniz Teknik Üniversitesi", "Trakya Üniversitesi", "Ondokuz Mayıs Üniversitesi",
    "Selçuk Üniversitesi", "Atatürk Üniversitesi", "Erciyes Üniversitesi",
    "İnönü Üniversitesi", "Fırat Üniversitesi", "Dicle Üniversitesi",
    "Van Yüzüncü Yıl Üniversitesi", "Kocaeli Üniversitesi"
]

# Standart fakülte/bölüm/ders yapısı
STANDARD_STRUCTURE = {
    "Mühendislik Fakültesi": {
        "Bilgisayar Mühendisliği": [
            "Programlama Dilleri", "Veri Yapıları", "Algoritma Analizi",
            "Yazılım Mühendisliği", "Veritabanı Sistemleri"
        ],
        "Elektrik-Elektronik Mühendisliği": [
            "Devre Analizi", "Sinyaller ve Sistemler", "Elektromanyetik Teori"
        ]
    },
    "İktisat Fakültesi": {
        "İktisat": [
            "Mikroekonomi", "Makroekonomi", "Ekonometri", "Para Teorisi"
        ],
        "İşletme": [
            "Muhasebe", "Finansal Yönetim", "Pazarlama", "Yönetim"
        ]
    }
}


def create_university_structure(uni_name, structure):
    """Üniversite yapısını oluştur"""
    uni, created = University.objects.get_or_create(name=uni_name)
    if created:
        print(f"✅ Üniversite oluşturuldu: {uni_name}")
    else:
        print(f"ℹ️  Üniversite zaten var: {uni_name}")
    
    for fakulte_name, bolumler in structure.items():
        fac, _ = Faculty.objects.get_or_create(university=uni, name=fakulte_name)
        
        for bolum_name, dersler in bolumler.items():
            dept, _ = Department.objects.get_or_create(faculty=fac, name=bolum_name)
            
            for ders_name in dersler:
                Course.objects.get_or_create(department=dept, name=ders_name)
    
    print(f"   → {len(structure)} fakülte, toplam {sum(len(b) for b in structure.values())} bölüm eklendi")


def main():
    print("🚀 30 Üniversite Verisi Yükleme Başladı...\n")
    
    # Detaylı yapıları olan üniversiteler
    for uni_name, structure in UNIVERSITIES_DATA.items():
        create_university_structure(uni_name, structure)
        print()
    
    # Kalan üniversiteler için standart yapı
    for uni_name in ADDITIONAL_UNIVERSITIES:
        create_university_structure(uni_name, STANDARD_STRUCTURE)
        print()
    
    print("🎉 Tüm üniversiteler başarıyla yüklendi!")
    print(f"\n📊 Özet:")
    print(f"   - Toplam Üniversite: {University.objects.count()}")
    print(f"   - Toplam Fakülte: {Faculty.objects.count()}")
    print(f"   - Toplam Bölüm: {Department.objects.count()}")
    print(f"   - Toplam Ders: {Course.objects.count()}")


if __name__ == '__main__':
    main()

