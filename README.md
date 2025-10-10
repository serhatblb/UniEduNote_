# 🎓 UniEduNote — Akademik Not Paylaşım Platformu

## 📘 Proje Özeti

**UniEduNote**, üniversite öğrencilerinin ders notlarını, ödev çözümlerini ve sınav içeriklerini organize bir biçimde paylaşabileceği, katkı sağladıkça puan ve ödül kazanabileceği bir **akademik topluluk platformudur.**

Platformun amacı, öğrenciler arasında bilgi paylaşımını teşvik etmek, kaliteli notların öne çıkmasını sağlamak ve katkıda bulunan kullanıcıları ödüllendirmektir.

---

## 🧱 Teknoloji Yığını

| Katman | Teknoloji |
|:--|:--|
| **Backend** | Django 5.2 + Django ORM |
| **Frontend** | HTML5, CSS3, Bootstrap (şimdilik), Responsive UI |
| **Veritabanı** | SQLite (geliştirme) → PostgreSQL (production) |
| **Kimlik Doğrulama** | Django Auth + planlanan e-posta doğrulaması |
| **Depolama** | Django FileField (PDF, Word, Image dosyaları) |
| **Gelecek API** | Django REST Framework (mobil sürüm için) |

---

## ✨ Şu Ana Kadar Tamamlanan Özellikler

### 🧍 Kullanıcı Sistemi
- Kayıt olma ve giriş yapma ekranları (modern ve responsive)
- JWT’siz, native Django auth tabanlı oturum sistemi
- Sidebar menü (dinamik olarak kullanıcı giriş durumuna göre değişiyor)
- Logout mekanizması

### 📂 Not Yönetimi
- Not yükleme formu  
  > Üniversite → Fakülte → Bölüm → Dönem → Ders zinciri seçimi  
  > Başlık, açıklama, dosya (PDF, Word, Image) alanları
- Not listeleme ekranı  
  > Kart tasarımı, indirme butonu, filtreleme (üniversite/bölüm/ders bazlı)
- Not detay ekranı  
  > Açıklama, yükleyen kullanıcı, indirme sayısı
- İndirme sayısı otomatik artış sistemi

### 👤 Profil & Dashboard
- Kullanıcı bilgileri görüntüleme (kullanıcı adı, mail, üniversite)
- Toplam yüklenen not sayısı, toplam indirme istatistiği
- Sidebar üzerinden profil ve dashboard geçişleri

---

## 🚧 Şu Anda Geliştirme Aşamasında Olanlar

### 🔒 1. **Kullanıcı Doğrulama & Güvenlik Sistemi**
- Kayıt sonrası e-posta ile doğrulama (aktif olmayan kullanıcılar giriş yapamaz)
- E-posta aktivasyon token yapısı
- Şifre sıfırlama (“Şifremi Unuttum” mail sistemi)
- Profil bilgilerini düzenleme (mail, şifre, üniversite)
- Giriş validation (sadece doğrulanmış kullanıcılar erişim sağlar)
- Girişsiz kullanıcılar not indiremez / yükleyemez

---

## 🏅 Planlanan Özellikler (Sonraki Fazlar)

### 🌟 Puan ve Ödül Sistemi (Gamification)
- Her eyleme göre puan kazanma:
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
- Otomatik puan hesaplama (`signals.py` desteği)
- Ödül tablosu ve ilerleme çubuğu

---

### 💬 Topluluk & Etkileşim Modülü
- Not yorum sistemi
- “Beğen” butonu (faydalı notları öne çıkarır)
- “Şikayet et” bildirimi (editör onayına düşer)
- Chat sistemi (not sahibine mesaj gönderimi)
- Bildirim ikonu (🔔) ile etkileşim uyarıları

---

### 🖥️ Dashboard Geliştirmeleri
- “Bu haftanın en çok indirilen notları” bölümü
- Yeni katılan üyeler listesi
- XP ilerleme çubuğu
- Grafiklerle performans ve katkı gösterimi

---

### 🤖 Gelecek Modüller (AI & Mobil)
- **PDF OCR + metin arama:** PDF içinde kelime bazlı arama
- **AI özetleme:** Not içeriklerinin GPT ile özetlenmesi
- **Mobil uygulama (Flutter):** REST API üzerinden tam entegrasyon
- **Doğrulanmış eğitmen rozetleri:** Üniversite e-posta adresiyle doğrulanan akademisyenler için

---

## 🗺️ Geliştirme Planı (Sıralı Yol Haritası)

| Sıra | Modül | Durum |
|------|--------|--------|
| 1️⃣ | Mail doğrulama sistemi | ⏳ Başlıyor |
| 2️⃣ | Şifre sıfırlama / Profil güncelleme | 🔜 |
| 3️⃣ | Giriş validation & erişim kontrolü | 🔜 |
| 4️⃣ | Puan / seviye / ödül sistemi | 🔜 |
| 5️⃣ | Dashboard & istatistik grafikleri | 🔜 |
| 6️⃣ | Topluluk modülü (yorum, beğeni, mesajlaşma) | 🔜 |
| 7️⃣ | Mobil API + AI modülü | 🚧 Uzun vadeli |

---

## 👨‍💻 Katkı & Geliştirici Notu

Proje şu anda **aktif geliştirme** sürecinde.  
Kodlar modüler olacak şekilde bölünmektedir:  
- `users` → kullanıcı, auth, profil işlemleri  
- `notes` → not yükleme, filtreleme, detay  
- `categories` → üniversite/fakülte/bölüm/ders modelleri  
- `rewards` → puan ve ödül sistemi (gelecek faz)  
- `chat` → mesajlaşma modülü (gelecek faz)

> Bu proje Django’nun tam potansiyelini kullanarak hem akademik hem sosyal bir ortam oluşturmayı hedeflemektedir.

---

## 📧 İletişim

**Geliştirici:** Serhat Bülbül  
📍 Türkiye  
🔗 GitHub: [https://github.com/serhatblb](https://github.com/serhatblb)

---

> “Bilgi paylaştıkça çoğalır.”  
> — UniEduNote Ekibi
