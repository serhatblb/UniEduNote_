# 🎓 UniEduNote — Akademik Not Paylaşım Platformu

## 📘 Proje Özeti

**UniEduNote**, üniversite öğrencilerinin ders notlarını, ödev çözümlerini ve sınav içeriklerini paylaşabileceği, katkı sağladıkça puan ve ödül kazanabileceği bir **akademik topluluk platformudur.**

Platformun hedefi, öğrenciler arasında bilgi paylaşımını kolaylaştırmak, kaliteli notların öne çıkmasını sağlamak ve katkı sağlayan kullanıcıları ödüllendirmektir.

---

## 🧱 Teknoloji Yığını

| Katman | Teknoloji |
|:--|:--|
| **Backend** | Django 5.2 + Django ORM |
| **Frontend** | HTML5, CSS3 (Tailwind tarzı modern sade tasarım) |
| **Veritabanı** | SQLite (geliştirme) → PostgreSQL (production) |
| **API** | Django REST Framework + JWT (SimpleJWT) |
| **Kimlik Doğrulama** | Django Auth + JWT + E-posta Aktivasyonu |
| **Depolama** | Django FileField (PDF, Word, Image dosyaları) |
| **Mail Servisi** | Gmail SMTP (şu anda console backend ile test) |

---

## ✨ Şu Ana Kadar Tamamlanan Özellikler

### 🧍 Kullanıcı Sistemi
- Modern ve responsive **Kayıt / Giriş ekranları**
- JWT tabanlı **API login** + Django **session entegrasyonu**
- **E-posta aktivasyonu:**  
  - Yeni kayıt olan kullanıcıya doğrulama linki gönderiliyor  
  - Aktivasyon yapılmadan giriş yapılamıyor
- **Sidebar menü**: kullanıcı giriş durumuna göre dinamik olarak değişiyor
- **Session login sistemi:**  
  - JWT token alınır  
  - Ardından Django session başlatılarak web tarafında oturum açılır  
  - Tarayıcıda `sessionid` cookie oluşur
- Logout ve yönlendirme mekanizmaları (dashboard / ana sayfa geçişleri)

---

### 📂 Not Yönetimi
- Not yükleme formu  
  > Üniversite → Fakülte → Bölüm → Dönem → Ders zinciri seçimi  
  > Başlık, açıklama, dosya (PDF, Word, Image) alanları  
- Not listeleme ekranı  
  > Kart görünümü + indirme butonu + dinamik filtreleme  
- Not detay ekranı  
  > Açıklama, yükleyen kullanıcı, indirme sayısı  
- İndirme sayısı otomatik artış sistemi

---

### 👤 Profil & Dashboard
- Dashboard: Not yükleme, not keşfetme, profil erişimi kartları  
- Profil sayfası: Kullanıcı bilgileri, yüklenen notlar ve toplam indirme sayısı  
- Sidebar üzerinden profil ve dashboard geçişleri

---

## 🔐 Şu Anda Geliştirme Aşamasında Olanlar

### 🔒 Kullanıcı Doğrulama & Güvenlik Sistemi
- [✅] **E-posta aktivasyon sistemi**  
- [✅] **Session tabanlı login (JWT + Django session birleşimi)**  
- [⏳] **Şifre sıfırlama (e-posta ile)**  
- [🔜] **Profil bilgilerini düzenleme (mail, şifre, üniversite, vs.)**  
- [🔜] **Login validation (sadece aktif kullanıcı erişebilir)**  
- [🔜] **Login olmadan not indirme/yükleme engeli**

---

## 🏅 Planlanan Özellikler (Sonraki Fazlar)

### 🌟 Puan ve Ödül Sistemi (Gamification)
- Puan kazanma:
  - +10 → Not yükleme  
  - +2 → Not indirildiğinde  
  - +5 → Beğeni  
  - −10 → Şikayet onaylandığında
- Puan bazlı seviye sistemi:
  | Puan | Seviye | Ünvan |
  |------|---------|--------|
  | 0–49 | ⭐ | Başlangıç |
  | 50–149 | ⭐⭐ | Katkıcı |
  | 150–299 | ⭐⭐⭐ | Güvenilir Katılımcı |
  | 300+ | ⭐⭐⭐⭐ | Elit Akademisyen |
- Ödül tablosu, ilerleme çubuğu, seviye ikonları  
- Otomatik puan hesaplama (`signals.py`)

---

### 💬 Topluluk & Etkileşim Modülü
- Not yorum sistemi  
- “Beğen” ve “Şikayet Et” butonları  
- Chat sistemi (not sahibine mesaj gönderimi)  
- Bildirim ikonu (🔔) ile etkileşim uyarıları  

---

### 🖥️ Dashboard Geliştirmeleri
- Haftalık en çok indirilen notlar  
- Yeni katılan üyeler listesi  
- XP ilerleme çubuğu  
- Grafiklerle katkı istatistikleri

---

### 🤖 Gelecek Modüller (AI & Mobil)
- PDF OCR + içerik arama  
- AI destekli not özetleme  
- Mobil uygulama (Flutter) → REST API entegrasyonu  
- Üniversite e-postasıyla doğrulanan “Akademisyen Rozeti”

---

## 🗺️ Geliştirme Yol Haritası

| Sıra | Modül | Durum |
|------|--------|--------|
| 1️⃣ | JWT + E-posta aktivasyon sistemi | ✅ Tamamlandı |
| 2️⃣ | Şifre sıfırlama / Profil düzenleme | ⏳ Başlayacak |
| 3️⃣ | Erişim validation ve güvenlik kontrolleri | 🔜 |
| 4️⃣ | Puan / seviye / ödül sistemi | 🔜 |
| 5️⃣ | Dashboard grafik ve istatistik | 🔜 |
| 6️⃣ | Topluluk (yorum / beğeni / mesajlaşma) | 🔜 |
| 7️⃣ | Mobil API + AI entegrasyonu | 🚧 Uzun vadeli |

---

## 👨‍💻 Geliştirici Notu

Kod yapısı modüler şekilde ayrılmıştır:  
- `users/` → kullanıcı, kimlik doğrulama, profil  
- `notes/` → not yükleme, listeleme, detay  
- `categories/` → üniversite, fakülte, bölüm, ders modelleri  
- `rewards/` → puan ve ödül sistemi (gelecek faz)  
- `chat/` → mesajlaşma modülü (gelecek faz)

> Proje, Django’nun hem klasik web hem modern REST altyapısını birleştirerek ölçeklenebilir, kurumsal düzeyde bir akademik paylaşım platformu oluşturmayı hedefliyor.

---

## 📧 İletişim

**Geliştirici:** Serhat Bülbül  
📍 Türkiye  
🔗 GitHub: [https://github.com/serhatblb](https://github.com/serhatblb)

---

> “Bilgi paylaştıkça çoğalır.”  
> — UniEduNote Ekibi
