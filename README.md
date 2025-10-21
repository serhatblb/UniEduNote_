# 🎓 UniEduNote — Akademik Not Paylaşım Platformu

## 📘 Proje Özeti
**UniEduNote**, öğrencilerin ders notlarını paylaşabildiği, yorum yapıp beğenerek etkileşime girdiği, katkı sağladıkça puan ve ödül kazandığı bir akademik topluluk platformudur.

---

## 🧱 Teknoloji Yığını
| Katman | Teknoloji |
|:--|:--|
| **Backend** | Django 5.2 + Django ORM |
| **Frontend** | HTML5, CSS3 (modern sade tasarım) |
| **Veritabanı** | SQLite (dev) → PostgreSQL (prod) |
| **API** | Django REST Framework + JWT (SimpleJWT) |
| **Auth** | Django Auth + JWT + E-posta aktivasyonu |
| **Depolama** | FileField (PDF, Word, Image) |
| **Mail** | Gmail SMTP (şimdilik console backend) |

---

## ✨ Tamamlanan Özellikler

### 🧍 Kullanıcı Sistemi
- JWT + Session tabanlı kimlik doğrulama  
- E-posta aktivasyon sistemi  
- Modern kayıt / giriş ekranları  
- Logout ve dashboard yönlendirmeleri  
- Şifre sıfırlama (e-posta bağlantısı ile)  
- Profil görüntüleme ve düzenleme ekranı  
  - Şifre değişimi destekleniyor  
  - E-posta değişimi geçici olarak kısıtlandı (ileride doğrulama eklenecek)  

### 📄 Not Yönetimi
- Not yükleme (dosya + açıklama)  
- Not listeleme (üniversite, bölüm, ders bazlı filtreleme)  
- Not detay ekranı (indir, yorum, beğeni, istatistik)  
- Not düzenleme ve silme (sadece not sahibi erişebilir)  
- Filtreli geri dön butonu (liste sayfasına filtreler korunarak dönüş)  

### 💬 Yorum & Beğeni Sistemi
- Her not için yorum ekleme, düzenleme, silme  
- Her not için beğeni (toggle + GET durumu)  
- Kullanıcı sadece kendi yorumlarını düzenleyip silebilir  
- Beğeni durumu giriş/çıkış sonrası da korunur (liste ve detay ekranlarında senkron)  
- Anlık yorum yenileme (sayfa yenilemeden liste güncellenir)  

### 🔒 Güvenlik & Erişim
- Giriş yapmadan `/dashboard/`, `/upload/`, `/notes/`, `/profile/` erişimi engellendi  
- JWT zorunluluğu (API’lerde `IsAuthenticated`)  
- `@login_required` ile tüm web view’lar koruma altında  
- Sadece içerik sahibi düzenleme ve silme işlemi yapabilir  

### 🎨 Görsel & UI
- Buton ve linklerde alt çizgi kaldırıldı  
- Modern mavi-beyaz tema  
- Responsive grid tabanlı kart yapısı  
- Hover efektleri ve sade animasyonlar  

---

## 🔧 Geliştirme Aşamasında
| Özellik | Durum |
|:--|:--|
| Şifre sıfırlama | ✅ |
| Profil düzenleme | ✅ |
| E-posta değişiklik doğrulama | 🔜 |
| Şifre geçmişi / tekrar kullanımı engelleme | 🔜 |
| Erişim kontrolü ve JWT entegrasyonu | ✅ |
| Not yükleme / düzenleme / silme | ✅ |
| Yorum & beğeni sistemi | ✅ |

---

## 🏅 Planlanan Özellikler

### 🌟 Puan & Ödül Sistemi
- Not yükleme, indirme, beğeni, yorum ile puan kazanma  
- Puan bazlı seviye sistemi (⭐ → ⭐⭐⭐⭐)  
- İlerleme çubuğu ve seviye ikonları  
- `signals.py` üzerinden otomatik puan hesaplama  

### 🏫 Kategori & Üniversite Yönetimi
- Üniversite, fakülte, bölüm ve ders listelerinin JSON / SQL kaynaktan yüklenmesi  
- Dinamik zincirleme dropdown (üniversite → fakülte → bölüm → ders)  
- Admin panelinden kategori ekleme / güncelleme  

### 🖥️ Dashboard Geliştirmeleri
- En çok indirilen notlar  
- Yeni üyeler listesi  
- İstatistik grafikleri ve XP barı  

### 🤖 Gelecek Faz
- AI destekli not özetleme  
- PDF OCR ve içerik arama  
- Mobil uygulama (Flutter)  
- Akademisyen rozet sistemi  

---

## 📅 Geliştirme Yol Haritası
| Sıra | Modül | Durum |
|------|--------|--------|
| 1️⃣ | JWT + E-posta aktivasyon | ✅ |
| 2️⃣ | Şifre sıfırlama / Profil düzenleme | ✅ |
| 3️⃣ | Erişim ve güvenlik (JWT validation) | ✅ |
| 4️⃣ | Not Yönetimi + Yorum & Beğeni | ✅ |
| 5️⃣ | Puan / ödül sistemi | 🔜 |
| 6️⃣ | Dashboard istatistikleri | 🔜 |
| 7️⃣ | Üniversite – fakülte – bölüm zinciri | 🔜 |
| 8️⃣ | Mobil + AI entegrasyonu | 🚧 |

---

## 🧩 Geliştirici Notları
- E-posta değişiklik doğrulaması **ilerleyen aşamada eklenecek.**  
- Şifre tekrar kullanımı ve geçmiş kontrolü **veritabanı fazında uygulanacak.**  
- Üniversite–fakülte–bölüm verileri büyük olduğu için **SQL tabanlı import planlanıyor.**

---

## 📧 İletişim
**Geliştirici:** Serhat Bülbül  
📍 Türkiye  
🔗 GitHub: [https://github.com/serhatblb](https://github.com/serhatblb)

---

> “Bilgi paylaştıkça çoğalır.”  
> — UniEduNote Ekibi  
