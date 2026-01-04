# 🎮 UniEduNote Gamification Sistemi - Tasarım Dokümantasyonu

## 📋 Genel Bakış

UniEduNote için tasarlanan kapsamlı oyunlaştırma sistemi, öğrencileri içerik üretmeye teşvik ederken adil ve sürdürülebilir bir rekabet ortamı oluşturur.

---

## 1️⃣ Temel Kavramlar

### XP (Experience Points) - Deneyim Puanı
- Kullanıcıların **toplam puanı** `UserProfile.total_xp` alanında tutulur
- Her puan hareketi `PointTransaction` modelinde loglanır
- Puanlar **geri alınamaz** (sadece ceza durumunda negatif puan verilebilir)

### Level (Seviye) Sistemi
- **Exponential Growth** algoritması kullanılır
- Her seviye bir öncekinden **%50 daha zor**
- Seviye hesaplama: `calculate_level()` metodu

### Seviye Tablosu

| Seviye | Gerekli Toplam XP | Seviye İçi XP | Rozet |
|--------|-------------------|---------------|-------|
| 1 | 0-99 | 0-99 | 🌱 Çaylak |
| 2 | 100-249 | 0-149 | 📚 Öğrenci |
| 3 | 250-474 | 0-224 | 🎓 Mezun |
| 4 | 475-811 | 0-336 | 👨‍🏫 Asistan |
| 5 | 812-1,316 | 0-504 | 🧠 Profesör |
| 6 | 1,317-2,073 | 0-756 | 👑 Dekan |
| 7 | 2,074-3,109 | 0-1,134 | 🌟 Rektör |
| 8+ | 3,110+ | - | 💎 Efsane |

**Formül:** 
- Level 1→2: 100 XP
- Level N→N+1: `previous_required * 1.5`

---

## 2️⃣ Puan Kazandıran Aksiyonlar

### Puan Tablosu

| Aksiyon | Puan | Açıklama | İstismar Önleme |
|---------|------|----------|-----------------|
| **Not Oluşturma** | +50 XP | İlk yükleme | Günde max 10 not |
| **Not Güncelleme** | +5 XP | Spam önleme için düşük | Her güncellemede |
| **Beğeni Alınması** | +2 XP | Her beğeni için | Kendi beğenisi sayılmaz |
| **İndirme Alınması** | +1 XP | Her indirme için | Kendi indirmesi sayılmaz |
| **Favoriye Eklenme** | +3 XP | İleride eklenecek | - |
| **Profil Tamamlama** | +20 XP | Tek seferlik | Üniversite + Avatar |
| **Günlük Giriş** | +5 XP | Günde bir kez | Seri takibi var |

### Örnek Senaryolar

#### Senaryo 1: Yeni Kullanıcı
- **Kayıt olur** → 0 XP, Level 1
- **Profil tamamlar** (üniversite + avatar) → +20 XP (Toplam: 20 XP, Level 1)
- **İlk notunu yükler** → +50 XP (Toplam: 70 XP, Level 1)
- **Notu 5 kez beğenilir** → +10 XP (Toplam: 80 XP, Level 1)
- **Notu 20 kez indirilir** → +20 XP (Toplam: 100 XP, **Level 2!** 🎉)

#### Senaryo 2: Aktif Kullanıcı
- **Level 3, 300 XP** (Level 4 için 175 XP kaldı)
- **5 not yükler** → +250 XP (Toplam: 550 XP, **Level 4!** 🎉)
- **Notları 50 beğeni alır** → +100 XP (Toplam: 650 XP, Level 4)
- **Günlük giriş yapar** → +5 XP (Toplam: 655 XP, Level 4)

---

## 3️⃣ İstismar Önleme Mekanizmaları

### Soft-Limit Yaklaşımı (Ceza YOK)

**Gerekçe:** Ceza puanı kullanıcıları demotive edebilir. Bunun yerine **soft-limit** kullanıyoruz:

1. **Günlük Not Limit:** Günde maksimum 10 not
   - Limit aşılırsa: Puan verilmez, uyarı gösterilir
   - Ertesi gün limit sıfırlanır

2. **Kendi İçeriğini Beğenme/İndirme:**
   - Kendi notunu beğenme: Puan verilmez
   - Kendi notunu indirme: Puan verilmez
   - `Like` modelinde `unique_together` ile zaten engellenmiş

3. **Düşük Kalite İçerik:**
   - Silinen notlar için ceza yok
   - Sadece puan verilmez (zaten verilmiş puan geri alınmaz)
   - İstatistiklerden düşülür

4. **Tekrar Beğeni/İndirme:**
   - Aynı kullanıcı aynı notu tekrar beğenemez (DB constraint)
   - Aynı kullanıcı aynı notu tekrar indirebilir ama puan verilmez

### İstismar Tespiti (İleride)

```python
# Örnek: Çok fazla silinen not varsa uyarı
if deleted_notes_count > created_notes_count * 0.5:
    # Uyarı ver, puan verme
    pass
```

---

## 4️⃣ Seviye Sistemi Algoritması

### Hesaplama Mantığı

```python
def calculate_level(total_xp):
    if total_xp < 100:
        return 1
    
    level = 1
    required_xp = 100  # Level 1→2
    current_xp = total_xp
    
    while current_xp >= required_xp:
        level += 1
        current_xp -= required_xp
        required_xp = int(required_xp * 1.5)  # %50 artış
    
    return level
```

### İlerleme Hesaplama

```python
def get_xp_progress(profile):
    # Mevcut seviye için gereken XP
    # Önceki seviyelere kadar gereken XP'yi çıkar
    # Kalan / Gereken = İlerleme yüzdesi
    return {
        'current': 75,      # Seviye içi mevcut XP
        'required': 150,    # Seviye için gereken XP
        'percentage': 50,   # İlerleme yüzdesi
        'remaining': 75     # Kalan XP
    }
```

---

## 5️⃣ Görsel & Psikolojik Etki

### Dashboard Gösterimi

1. **Seviye Rozeti:**
   - İkon + Renk + İsim
   - Level badge kartında gösterilir

2. **İlerleme Çubuğu:**
   - Animated progress bar
   - "X XP kaldı" mesajı
   - Shimmer efekti

3. **İstatistikler:**
   - Toplam Not, Beğeni, İndirme
   - Günlük Seri (streak)

4. **Son Puan Hareketleri:**
   - Son 5 işlem
   - Pozitif/Negatif renk kodlaması

### Motivasyon Stratejisi

- ✅ **İlk seviyeler hızlı:** Hemen seviye atlama hissi
- ✅ **"Az kaldı" hissi:** Progress bar ile görsel motivasyon
- ✅ **Rozetler:** Seviye bazlı rozetler
- ✅ **Günlük seri:** Süreklilik motivasyonu
- ❌ **Stres yok:** Ceza puanı yok, sadece limit

---

## 6️⃣ Teknik Mimari

### Backend Yapısı

#### Models
1. **UserProfile:** XP, Level, istatistikler
2. **PointTransaction:** Tüm puan hareketleri (audit log)
3. **Badge:** Rozetler (ileride genişletilebilir)

#### Gamification Modülü (`rewards/gamification.py`)
- `add_points()`: Puan ekleme ve loglama
- `handle_note_created()`: Not oluşturma işlemi
- `handle_like_received()`: Beğeni işlemi
- `handle_download_received()`: İndirme işlemi
- `handle_daily_login()`: Günlük giriş
- `get_leaderboard()`: Liderlik tablosu

#### Signal Handlers (`rewards/signals.py`)
- `note_created_or_updated`: Not oluşturma/güncelleme
- `like_created`: Beğeni oluşturma
- `note_deleted`: Not silme (istatistik güncelleme)

#### View Entegrasyonu
- `dashboard()`: Gamification bilgileri
- `download_note()`: İndirme puanı
- `profile()`: Profil tamamlama kontrolü

### Frontend Yapısı

#### Dashboard
- XP ve Level kartı
- Progress bar (animated)
- Seviye rozeti
- İstatistikler
- Son puan hareketleri

#### Performans
- `select_related()` ile N+1 query önleme
- `aggregate()` ile istatistik hesaplama
- Cache'lenebilir veriler (ileride)

---

## 7️⃣ Genişleyebilirlik

### Liderlik Tablosu
```python
# Tüm zamanlar
get_leaderboard(limit=10)

# Haftalık
get_leaderboard(limit=10, period='weekly')

# Aylık
get_leaderboard(limit=10, period='monthly')
```

### Bölüm/Ders Bazlı Sıralamalar
```python
# İleride eklenebilir
get_department_leaderboard(department_id, limit=10)
get_course_leaderboard(course_id, limit=10)
```

### Rozetler (Badges)
- ✅ İlk not (`first_note`)
- ✅ İlk beğeni (`first_like`)
- ✅ İlk indirme (`first_download`)
- ✅ 10/50/100 not (`notes_10`, `notes_50`, `notes_100`)
- ✅ 100 beğeni (`likes_100`)
- ✅ 1000 indirme (`downloads_1000`)
- ✅ Seviye 5/10 (`level_5`, `level_10`)
- ✅ 7/30 gün seri (`daily_streak_7`, `daily_streak_30`)

---

## 8️⃣ Özet Tablo

| Özellik | Değer | Açıklama |
|---------|-------|----------|
| **Not Oluşturma** | +50 XP | Günde max 10 |
| **Not Güncelleme** | +5 XP | Spam önleme |
| **Beğeni Alınması** | +2 XP | Kendi beğenisi yok |
| **İndirme Alınması** | +1 XP | Kendi indirmesi yok |
| **Profil Tamamlama** | +20 XP | Tek seferlik |
| **Günlük Giriş** | +5 XP | Günde bir kez |
| **Seviye Sistemi** | Exponential | %50 artış |
| **İstismar Önleme** | Soft-limit | Ceza yok |
| **Rozetler** | 12 tip | Otomatik verilir |

---

## 9️⃣ Kullanım Örnekleri

### Örnek 1: Yeni Kullanıcı İlk Hafta
```
Gün 1: Kayıt + Profil → 20 XP (Level 1)
Gün 1: 2 Not → 100 XP (Level 1)
Gün 2: Günlük giriş → 5 XP (105 XP, Level 1)
Gün 2: Notlar 10 beğeni → 20 XP (125 XP, Level 2! 🎉)
Gün 3: Günlük giriş → 5 XP (130 XP, Level 2)
Gün 3: 3 Not → 150 XP (280 XP, Level 2)
Gün 4-7: Günlük giriş serisi → 20 XP (300 XP, Level 3! 🎉)
```

### Örnek 2: Aktif İçerik Üreticisi
```
Mevcut: Level 5, 1,500 XP
Hafta içi: Günde 5 not → 250 XP/gün
Hafta sonu: Günde 10 not (limit) → 500 XP/gün
Toplam hafta: ~2,000 XP
Yeni seviye: Level 6! 👑
```

---

## 🔟 Sonuç

Bu sistem:
- ✅ **Adil:** İstismar önleme mekanizmaları var
- ✅ **Motivasyon:** İlk seviyeler hızlı, görsel feedback
- ✅ **Sürdürülebilir:** Soft-limit, ceza yok
- ✅ **Genişletilebilir:** Rozetler, liderlik tabloları
- ✅ **Performanslı:** Optimize edilmiş sorgular
- ✅ **Şeffaf:** Tüm puan hareketleri loglanır

**Sistem hazır ve çalışır durumda!** 🚀

