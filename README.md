# 🎓 UniEduNote — Akademik Not Paylaşım Platformu

## 📘 Proje Özeti
**UniEduNote**, öğrencilerin ders notlarını paylaşabileceği, katkı sağladıkça puan ve ödül kazandığı bir akademik topluluk platformudur.

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
- Şifre sıfırlama akışı (e-posta bağlantısı ile)
- Profil görüntüleme ve düzenleme ekranı  
  - Şifre değişimi destekleniyor  
  - E-posta değişimi geçici olarak kısıtlandı (gelecekte doğrulama eklenecek)

### 🔒 Güvenlik & Erişim
- Giriş yapmadan `/dashboard/`, `/upload/`, `/notes/`, `/profile/` erişimi engellendi  
- JWT zorunluluğu getirildi (API’lerde `IsAuthenticated`)  
- `@login_required` ile tüm web view’lar koruma altında

---

## 🔧 Geliştirme Aşamasında
| Özellik | Durum |
|:--|:--|
| Şifre sıfırlama akışı | ✅ Tamamlandı |
| Profil düzenleme | ✅ Tamamlandı |
| E-posta değişiklik doğrulama | 🔜 Eklenecek |
| Şifre geçmişi / tekrar kullanımı engelleme | 🔜 Eklenecek |
| Erişim kontrolü ve JWT entegrasyonu | ✅ Tamamlandı |

---

## 🏅 Planlanan Özellikler
### 🌟 Puan & Ödül Sistemi
- Not yükleme, indirme, beğeni, şikayet ile puan kazanma  
- Puan bazlı seviye sistemi (⭐ → ⭐⭐⭐⭐)  
- İlerleme çubuğu ve seviye ikonları  
- `signals.py` üzerinden otomatik puan hesaplama  

### 💬 Topluluk Modülü
- Not yorumları ve beğeniler  
- Şikayet ve bildirim sistemi  
- Sohbet (chat) özelliği

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
| 4️⃣ | Puan / ödül sistemi | 🔜 |
| 5️⃣ | Dashboard istatistikleri | 🔜 |
| 6️⃣ | Yorum / Beğeni / Chat | 🔜 |
| 7️⃣ | Mobil + AI entegrasyonu | 🚧 |

---

## 🧩 Geliştirici Notları
- E-posta değişiklik doğrulaması **ilerleyen aşamada eklenecek**
- Şifre tekrar kullanımı ve geçmiş kontrolü **veritabanı fazında uygulanacak**

---

## 📧 İletişim

**Geliştirici:** Serhat Bülbül  
📍 Türkiye  
🔗 GitHub: [https://github.com/serhatblb](https://github.com/serhatblb)

---

> “Bilgi paylaştıkça çoğalır.”  
> — UniEduNote Ekibi