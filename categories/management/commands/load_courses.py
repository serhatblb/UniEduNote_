"""
Tüm bölümlere ders yükler.
- Evrensel dersler: her bölüme eklenir
- Alan dersleri: bölüm adı anahtar kelimeye göre eşleştirilir

Kullanım:
    python manage.py load_courses           # sadece eksik dersleri ekle
    python manage.py load_courses --clear   # önce temizle, sonra ekle
"""
from django.core.management.base import BaseCommand
from categories.models import Department, Course

# ─── Evrensel dersler (her bölüme) ───────────────────────────────────────────
UNIVERSAL = [
    "Türk Dili I",
    "Türk Dili II",
    "Atatürk İlkeleri ve İnkılap Tarihi I",
    "Atatürk İlkeleri ve İnkılap Tarihi II",
    "Yabancı Dil I (İngilizce)",
    "Yabancı Dil II (İngilizce)",
]

# ─── Alan dersleri: (anahtar kelimeler, ders listesi) ─────────────────────────
FIELD_COURSES = [
    # ── Genel Mühendislik ──────────────────────────────────────────────────────
    (
        ["mühend"],
        [
            "Matematik I", "Matematik II", "Fizik I", "Fizik II",
            "Kimya", "Lineer Cebir", "Diferansiyel Denklemler",
            "Olasılık ve İstatistik", "Teknik Resim", "Mühendislik Etiği",
        ],
    ),
    # ── Bilgisayar / Yazılım / Bilişim ────────────────────────────────────────
    (
        ["bilgisayar", "yazılım", "bilişim", "siber"],
        [
            "Programlamaya Giriş", "Veri Yapıları ve Algoritmalar",
            "Nesne Yönelimli Programlama", "Veritabanı Sistemleri",
            "Bilgisayar Ağları", "İşletim Sistemleri",
            "Yazılım Mühendisliği", "Web Programlama",
            "Yapay Zeka ve Makine Öğrenmesi", "Mobil Uygulama Geliştirme",
            "Veri Madenciliği", "Bulut Bilişim",
        ],
    ),
    # ── Elektrik / Elektronik ─────────────────────────────────────────────────
    (
        ["elektrik", "elektronik", "biyomedikal"],
        [
            "Devre Analizi", "Elektronik I", "Elektronik II",
            "Elektromanyetik Teori", "Dijital Sistemler",
            "Kontrol Sistemleri", "Sinyal ve Sistemler",
            "Güç Sistemleri", "Mikrodenetleyiciler",
        ],
    ),
    # ── Makine ────────────────────────────────────────────────────────────────
    (
        ["makine", "mekatronik", "otomoti"],
        [
            "Termodinamik I", "Termodinamik II", "Akışkanlar Mekaniği",
            "Makine Elemanları I", "Makine Elemanları II",
            "Mukavemet", "İmalat Yöntemleri", "Kontrol Mühendisliği",
            "Isı Transferi",
        ],
    ),
    # ── İnşaat ────────────────────────────────────────────────────────────────
    (
        ["inşaat", "jeodezi", "harita", "jeofizik"],
        [
            "Statik", "Dinamik", "Zemin Mekaniği", "Betonarme",
            "Çelik Yapılar", "Ulaştırma Mühendisliği",
            "Su Kaynakları Mühendisliği", "Yapı Malzemesi",
        ],
    ),
    # ── Tıp / Sağlık ──────────────────────────────────────────────────────────
    (
        ["tıp", "hemsir", "hemşir", "ebelik", "eczac", "diş", "sağlık"],
        [
            "Anatomi", "Fizyoloji", "Histoloji ve Embriyoloji",
            "Biyokimya", "Mikrobiyoloji ve Viroloji", "Patoloji",
            "Farmakoloji", "Dahiliye", "Cerrahi", "Pediatri",
            "Kadın Hastalıkları ve Doğum", "Psikiyatri",
            "Halk Sağlığı", "Tıp Etiği",
        ],
    ),
    # ── Hukuk ─────────────────────────────────────────────────────────────────
    (
        ["hukuk"],
        [
            "Hukuka Giriş", "Anayasa Hukuku", "Medeni Hukuk",
            "Borçlar Hukuku Genel", "Borçlar Hukuku Özel",
            "Ceza Hukuku Genel", "Ceza Hukuku Özel",
            "Ticaret Hukuku", "İdare Hukuku", "Devletler Özel Hukuku",
            "İş Hukuku", "Medeni Usul Hukuku",
        ],
    ),
    # ── İşletme ───────────────────────────────────────────────────────────────
    (
        ["işletme", "yönetim", "ticaret"],
        [
            "İşletmeye Giriş", "Muhasebe I", "Muhasebe II",
            "Mikro İktisat", "Makro İktisat", "Finans",
            "Pazarlama Yönetimi", "İnsan Kaynakları Yönetimi",
            "Üretim Yönetimi", "Stratejik Yönetim",
            "Girişimcilik", "Proje Yönetimi",
        ],
    ),
    # ── İktisat ───────────────────────────────────────────────────────────────
    (
        ["iktisat", "ekonomi"],
        [
            "Mikro İktisat I", "Mikro İktisat II",
            "Makro İktisat I", "Makro İktisat II",
            "Matematiksel İktisat", "Ekonometri",
            "Para Teorisi ve Politikası", "Uluslararası İktisat",
            "Kalkınma İktisadı", "Sanayi İktisadı",
        ],
    ),
    # ── Psikoloji ─────────────────────────────────────────────────────────────
    (
        ["psikoloji"],
        [
            "Psikolojiye Giriş", "Deneysel Psikoloji",
            "Klinik Psikoloji", "Sosyal Psikoloji",
            "Gelişim Psikolojisi", "Kişilik Teorileri",
            "Psikolojik Ölçme ve Değerlendirme",
            "Öğrenme Psikolojisi", "Nöropsikoloji",
        ],
    ),
    # ── Eğitim / Öğretmenlik ──────────────────────────────────────────────────
    (
        ["eğitim", "öğretmen", "pedagoji"],
        [
            "Eğitime Giriş", "Eğitim Psikolojisi",
            "Öğretim İlke ve Yöntemleri", "Ölçme ve Değerlendirme",
            "Sınıf Yönetimi", "Öğretmenlik Uygulaması I",
            "Öğretmenlik Uygulaması II", "Rehberlik",
            "Eğitimde Araştırma Yöntemleri", "Özel Eğitim",
        ],
    ),
    # ── Matematik ─────────────────────────────────────────────────────────────
    (
        ["matematik"],
        [
            "Analiz I", "Analiz II", "Analiz III",
            "Lineer Cebir", "Diferansiyel Denklemler",
            "Soyut Cebir", "Topoloji", "Sayısal Analiz",
            "Kompleks Analiz", "Diferansiyel Geometri",
            "Olasılık Teorisi",
        ],
    ),
    # ── Fizik ─────────────────────────────────────────────────────────────────
    (
        ["fizik"],
        [
            "Genel Fizik I", "Genel Fizik II",
            "Klasik Mekanik", "Elektromanyetizma",
            "Kuantum Mekaniği I", "Kuantum Mekaniği II",
            "Termodinamik ve İstatistik Fizik",
            "Katıhal Fiziği", "Nükleer Fizik",
            "Optik",
        ],
    ),
    # ── Kimya ─────────────────────────────────────────────────────────────────
    (
        ["kimya"],
        [
            "Genel Kimya I", "Genel Kimya II",
            "Organik Kimya I", "Organik Kimya II",
            "Analitik Kimya", "Fiziksel Kimya I", "Fiziksel Kimya II",
            "Biyokimya", "Polimer Kimyası", "Enstrümental Analiz",
        ],
    ),
    # ── Biyoloji ──────────────────────────────────────────────────────────────
    (
        ["biyoloji", "biyoteknoloji", "biyomühend", "genetik"],
        [
            "Biyolojiye Giriş", "Hücre Biyolojisi", "Genetik",
            "Ekoloji", "Botanik", "Zooloji",
            "Mikrobiyoloji", "Moleküler Biyoloji",
            "Biyokimya", "Evrim",
        ],
    ),
    # ── Mimarlık ──────────────────────────────────────────────────────────────
    (
        ["mimarlık", "mimar", "kentsel", "şehir"],
        [
            "Mimari Tasarım I", "Mimari Tasarım II",
            "Mimari Tasarım III", "Mimari Tasarım IV",
            "Yapı Bilgisi I", "Yapı Bilgisi II",
            "Mimarlık Tarihi", "Statik",
            "Bilgisayar Destekli Tasarım", "Kentsel Tasarım",
        ],
    ),
    # ── Maliye / Kamu Yönetimi ────────────────────────────────────────────────
    (
        ["maliye", "kamu yönetimi", "siyaset"],
        [
            "Kamu Maliyesi", "Vergi Hukuku", "Bütçe Teorisi ve Uygulaması",
            "İdare Hukuku", "Mali Hukuk", "Siyasi Düşünceler Tarihi",
            "Kamu Politikası", "Yerel Yönetimler",
        ],
    ),
    # ── Sosyoloji ─────────────────────────────────────────────────────────────
    (
        ["sosyoloji", "antropoloji"],
        [
            "Sosyolojiye Giriş", "Klasik Sosyoloji Teorileri",
            "Çağdaş Sosyoloji Teorileri", "Sosyal Araştırma Yöntemleri",
            "Kentleşme Sosyolojisi", "Aile Sosyolojisi",
            "Suç Sosyolojisi", "Siyaset Sosyolojisi",
        ],
    ),
    # ── İletişim / Medya ──────────────────────────────────────────────────────
    (
        ["iletişim", "medya", "gazete", "halkla"],
        [
            "İletişime Giriş", "Medya ve Toplum",
            "Gazetecilik", "Halkla İlişkiler",
            "Reklamcılık", "Dijital Medya",
            "Radyo ve Televizyon", "Fotoğrafçılık",
        ],
    ),
    # ── Tarih ─────────────────────────────────────────────────────────────────
    (
        ["tarih"],
        [
            "Tarihe Giriş", "Osmanlı Tarihi I", "Osmanlı Tarihi II",
            "Cumhuriyet Tarihi", "Orta Çağ Tarihi",
            "Yeni Çağ Tarihi", "Tarih Metodolojisi",
            "Türk Kültür Tarihi", "İslam Tarihi",
        ],
    ),
    # ── Uluslararası İlişkiler ────────────────────────────────────────────────
    (
        ["uluslararası ilişki", "dış politika"],
        [
            "Uluslararası İlişkilere Giriş", "Uluslararası Hukuk",
            "Türk Dış Politikası", "Avrupa Birliği",
            "Uluslararası Örgütler", "Diplomatik Tarih",
            "Güvenlik Çalışmaları",
        ],
    ),
    # ── Finans / Bankacılık ───────────────────────────────────────────────────
    (
        ["finans", "bankacılık", "sigortacılık"],
        [
            "Finansal Yönetim", "Sermaye Piyasaları",
            "Bankacılık", "Sigortacılık", "Türev Ürünler",
            "Portföy Yönetimi", "Finansal Muhasebe",
            "Risk Yönetimi",
        ],
    ),
    # ── Turizm / Otelcilik ────────────────────────────────────────────────────
    (
        ["turizm", "otelcilik", "gastronomi", "konaklama"],
        [
            "Turizme Giriş", "Konaklama İşletmeciliği",
            "Seyahat Acentacılığı", "Yiyecek İçecek Yönetimi",
            "Turizm Hukuku", "Turizm Pazarlaması",
            "Destinasyon Yönetimi",
        ],
    ),
    # ── Hemşirelik / Sağlık Yönetimi (ayrı) ──────────────────────────────────
    (
        ["sağlık yönetimi", "sağlık yönetim"],
        [
            "Sağlık Hizmetleri Yönetimi", "Hastane İşletmeciliği",
            "Sağlık Hukuku", "Sağlık Ekonomisi",
            "Kalite Yönetimi", "Tıbbi Terminoloji",
        ],
    ),
]


class Command(BaseCommand):
    help = "Tüm bölümlere ders yükler (evrensel + alan dersleri)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Önce tüm dersleri sil, sonra yükle",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Course.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"{deleted} ders silindi."))

        departments = list(Department.objects.all().only("id", "name"))
        self.stdout.write(f"{len(departments)} bölüm bulundu.")

        # Mevcut (dept_id, name) çiftlerini çek — duplicate ekleme
        existing = set(Course.objects.values_list("department_id", "name"))

        to_create = []

        for dept in departments:
            name_lower = dept.name.lower()

            # 1. Evrensel dersler
            for course_name in UNIVERSAL:
                if (dept.id, course_name) not in existing:
                    to_create.append(Course(department_id=dept.id, name=course_name))

            # 2. Alan dersleri
            for keywords, course_names in FIELD_COURSES:
                if any(kw in name_lower for kw in keywords):
                    for course_name in course_names:
                        if (dept.id, course_name) not in existing:
                            to_create.append(Course(department_id=dept.id, name=course_name))

        # Batch insert
        BATCH = 2000
        total = 0
        for i in range(0, len(to_create), BATCH):
            batch = to_create[i : i + BATCH]
            Course.objects.bulk_create(batch, ignore_conflicts=True)
            total += len(batch)
            self.stdout.write(f"  {total}/{len(to_create)} ders eklendi...")

        self.stdout.write(self.style.SUCCESS(
            f"\nTamamlandı: {len(to_create)} ders eklendi. "
            f"Toplam: {Course.objects.count()} ders."
        ))
