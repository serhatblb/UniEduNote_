# 🎓 UniEduNote — Akademik Not Paylaşım Platformu

## 📘 Proje Özeti
**UniEduNote**, öğrencilerin ders notlarını güvenli bir bulut altyapısında paylaşabildiği, yorum ve beğenilerle etkileşime girdiği, dinamik ve modern bir akademik topluluk platformudur. Proje, yerel geliştirme ortamından çıkarılarak **modern Cloud Native mimari** ile canlıya alınmıştır.

---

## 🧱 Teknoloji Yığını & Altyapı
Modern ve ölçeklenebilir teknolojiler kullanılarak geliştirilmiştir.

| Katman | Teknoloji / Servis | Açıklama |
|:--|:--|:--|
| **Backend** | Django 5.x + Python | Ana uygulama çatısı |
| **Veritabanı** | **PostgreSQL (Neon.tech)** | Kalıcı veri saklama (Production) |
| **Dosya Depolama** | **Cloudinary** | Medya dosyaları (PDF, Resim) için bulut depolama |
| **Statik Dosyalar** | **WhiteNoise** | CSS/JS dosyalarının optimize sunumu |
| **Sunucu (Deploy)** | **Render** | PaaS (Platform as a Service) barındırma |
| **API** | DRF + SimpleJWT | RESTful API ve Token tabanlı güvenlik |
| **Frontend** | HTML5, CSS3, jQuery (AJAX) | Dinamik form yönetimi ve modern tasarım |
| **Mail Servisi** | SendGrid / SMTP | Aktivasyon ve bildirim mailleri |

---

## ✨ Tamamlanan Özellikler

### 🚀 Canlı Sistem & Altyapı (YENİ)
- **Render Deploy:** Proje canlı sunucuya taşındı (`gunicorn` ile).
- **Kalıcı Veritabanı:** Sunucu yeniden başlasa bile verilerin silinmemesi için PostgreSQL entegrasyonu yapıldı.
- **Bulut Depolama:** Yüklenen notların kaybolmaması için Cloudinary entegre edildi.
- **Veri Doldurma Botu:** `db_setup.py` scripti ile stratejik üniversite, fakülte ve bölümlerin tek komutla veritabanına yüklenmesi sağlandı.

### 🏫 Akıllı Kategori Yönetimi (YENİ)
- **AJAX Zincirleme Dropdown:** Not yüklerken Üniversite seçilince Fakültelerin, Fakülte seçilince Bölümlerin otomatik gelmesi sağlandı.
- **Stratejik Veri Yapısı:** AÖF ve en çok tercih edilen üniversiteler öncelikli olarak sisteme eklendi.

### 📄 Not Yönetimi
- **Bulut Tabanlı Yükleme:** PDF ve görseller direkt Cloudinary CDN üzerine yüklenir.
- **Güvenli İndirme:** Dosyalar yetkisiz erişime karşı korunur, indirme sayıları takip edilir.
- **Filtreleme:** Üniversite > Bölüm > Ders bazlı detaylı not arama.

### 🧍 Kullanıcı Sistemi
- JWT + Session tabanlı hibrit kimlik doğrulama.
- E-posta aktivasyon sistemi (SendGrid entegreli).
- Modern Dashboard ve Profil yönetimi.
- Kullanıcıya özel yüklenen notlar listesi.

### 💬 Etkileşim
- Yorum yapma ve silme (Anlık güncellenen arayüz).
- Beğeni sistemi (Like/Unlike).
- Sadece içerik sahibi tarafından düzenleme/silme yetkisi.

---

## 🔧 Kurulum & Geliştirme (Lokalde Çalıştırma)

Projeyi kendi bilgisayarınızda çalıştırmak için:

1.  **Depoyu klonlayın:**
    ```bash
    git clone https://github.com/serhatblb/UniEduNote.git
    cd UniEduNote
    ```

2.  **Sanal ortamı kurun ve paketleri yükleyin:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Çevre Değişkenlerini (.env) Ayarlayın:**
    *   `SECRET_KEY`, `DEBUG`, `DATABASE_URL` (Opsiyonel), `CLOUDINARY_` anahtarlarını ekleyin.

4.  **Veritabanını Hazırlayın:**
    ```bash
    python manage.py migrate
    python db_setup.py  # Üniversite verilerini otomatik yükler
    ```

5.  **Sunucuyu Başlatın:**
    ```bash
    python manage.py runserver
    ```

---

## 📅 Geliştirme Yol Haritası
| Sıra | Modül | Durum |
|------|--------|--------|
| 1️⃣ | JWT + E-posta aktivasyon | ✅ Tamamlandı |
| 2️⃣ | Cloudinary & PostgreSQL Geçişi | ✅ Tamamlandı |
| 3️⃣ | AJAX ile Dinamik Formlar | ✅ Tamamlandı |
| 4️⃣ | Render Deploy (Canlı Yayın) | ✅ Tamamlandı |
| 5️⃣ | Puan & Ödül Sistemi | 🔜 Sırada |
| 6️⃣ | Dashboard İstatistik Grafikleri | 🔜 Planlanıyor |
| 7️⃣ | Mobil Uygulama (Flutter) | 🚧 Ar-Ge Aşamasında |

---

## 🧩 Geliştirici Notları
- Proje **Django 5** standartlarına uygun `STORAGES` yapısına geçirilmiştir.
- Statik dosyalar için **WhiteNoise**, Medya dosyaları için **Cloudinary** hibrit yapısı kurulmuştur.
- Veritabanı bağlantısı `dj_database_url` ile ortam değişkenine göre (Localde SQLite, Canlıda Postgres) otomatik değişir.

---

## 📧 İletişim
**Geliştirici:** Serhat Bülbül  
📍 Türkiye  
🔗 GitHub: [https://github.com/serhatblb](https://github.com/serhatblb)

---

> “Bilgi paylaştıkça çoğalır.”  
> — UniEduNote Ekibi