# 🎮 Gamification Sistemi - Kurulum Rehberi

## Adım 1: Migrations Oluştur

```bash
# Virtual environment aktif et
source venv/bin/activate

# Migrations oluştur
python manage.py makemigrations rewards

# Migrations uygula
python manage.py migrate rewards
```

## Adım 2: Mevcut Kullanıcılar İçin Profil Oluştur

Mevcut kullanıcılar için otomatik profil oluşturma scripti:

```python
# manage.py shell içinde veya bir management command olarak
from users.models import User
from rewards.gamification import get_or_create_profile

for user in User.objects.all():
    profile = get_or_create_profile(user)
    print(f"{user.username} profili oluşturuldu: Level {profile.level}, {profile.total_xp} XP")
```

Veya management command olarak:

```bash
python manage.py shell
>>> from users.models import User
>>> from rewards.gamification import get_or_create_profile
>>> for user in User.objects.all():
...     get_or_create_profile(user)
```

## Adım 3: Test Et

1. **Yeni not yükle** → +50 XP kazanmalı
2. **Notu beğen** (başka kullanıcı) → Not sahibi +2 XP kazanmalı
3. **Notu indir** (başka kullanıcı) → Not sahibi +1 XP kazanmalı
4. **Dashboard'a git** → XP, Level, progress bar görünmeli
5. **Günlük giriş yap** → +5 XP kazanmalı

## Adım 4: Admin Panelinde Kontrol

Admin panelinde şunları görebilirsin:
- `Rewards > User Profiles` - Tüm kullanıcı profilleri
- `Rewards > Point Transactions` - Tüm puan hareketleri
- `Rewards > Badges` - Tüm rozetler

## Önemli Notlar

1. **Signal'lar otomatik çalışır** - Not oluşturma, beğeni gibi işlemlerde otomatik puan verilir
2. **İlk kullanıcılar için profil yoksa** - `get_or_create_profile()` otomatik oluşturur
3. **Eski puan sistemi** - User.rank property'si artık gamification sistemini kullanıyor

## Sorun Giderme

### Sorun: "UserProfile matching query does not exist"
**Çözüm:** Kullanıcı için profil oluştur:
```python
from rewards.gamification import get_or_create_profile
profile = get_or_create_profile(user)
```

### Sorun: "Signals çalışmıyor"
**Çözüm:** `rewards/apps.py` dosyasında `ready()` metodu var mı kontrol et:
```python
def ready(self):
    import rewards.signals
```

### Sorun: "Puanlar güncellenmiyor"
**Çözüm:** 
1. Signal'ların çalıştığını kontrol et
2. `PointTransaction` tablosunda kayıt var mı kontrol et
3. `UserProfile.total_xp` değerini kontrol et

## Performans İpuçları

1. **Liderlik tablosu için index:** `total_xp` ve `level` alanları zaten indexlenmiş
2. **Transaction logları:** Çok fazla log birikirse arşivlenebilir
3. **Cache:** Level badge'leri cache'lenebilir (ileride)

