# 🔍 Sunucuda DEBUG Ayarını Kontrol Etme Rehberi

## Adım 1: Sunucuya Bağlan
```bash
ssh root@sunucu-ip-adresi
# veya
ssh kullanici@sunucu-ip-adresi
```

## Adım 2: Proje Dizinine Git
```bash
cd /var/www/UniEduNote
```

## Adım 3: .env Dosyasını Kontrol Et

### Yöntem 1: .env Dosyasını Oku
```bash
cat .env | grep DEBUG
```

**Beklenen Çıktı:**
- `DEBUG=False` ✅ (Production için doğru)
- `DEBUG=True` ❌ (Production için yanlış)

### Yöntem 2: Tüm .env Dosyasını Görüntüle
```bash
cat .env
```

## Adım 4: Settings.py Dosyasını Kontrol Et (Opsiyonel)

Settings.py dosyası environment variable'dan okuyor, ama kontrol edebilirsin:

```bash
cat uniedunote/settings.py | grep -A 5 "DEBUG"
```

**Beklenen Çıktı:**
```python
DEBUG_ENV = os.environ.get("DEBUG", "False").lower()
DEBUG = DEBUG_ENV in ("true", "1", "yes")
```

Bu kod `.env` dosyasındaki `DEBUG` değerini okuyor.

## Adım 5: Python ile Kontrol Et (En Kesin Yöntem)

```bash
# Virtual environment'ı aktif et
source venv/bin/activate

# Django shell ile kontrol et
python manage.py shell
```

Django shell'de:
```python
from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
```

**Beklenen Çıktı:**
```
DEBUG: False
ALLOWED_HOSTS: ['your-domain.com', 'www.your-domain.com']
```

Çıkmak için:
```python
exit()
```

## Adım 6: .env Dosyasını Düzenle (Eğer DEBUG=True ise)

```bash
# Nano editör ile aç
nano .env

# DEBUG=False olarak değiştir
# Dosyayı kaydet: Ctrl+O, Enter, Ctrl+X
```

## Adım 7: Gunicorn'u Yeniden Başlat

```bash
systemctl restart gunicorn

# Veya
sudo systemctl restart gunicorn
```

## Adım 8: Kontrol Et (Web Tarayıcıdan)

1. Tarayıcıda sitenize gidin
2. Hata sayfası görüyorsanız ve detaylı hata mesajları varsa → `DEBUG=True` ❌
3. Sadece "500 Internal Server Error" gibi genel mesaj varsa → `DEBUG=False` ✅

## ⚠️ ÖNEMLİ NOTLAR

### Production'da DEBUG=False Olmalı Çünkü:
- ✅ Güvenlik: Hata mesajlarında hassas bilgiler gösterilmez
- ✅ Performans: Debug modu daha yavaştır
- ✅ Profesyonellik: Kullanıcıya teknik detaylar gösterilmez

### DEBUG=True Olduğunda Riskler:
- ❌ Veritabanı şemaları, kod yapısı gibi hassas bilgiler görülebilir
- ❌ Hata mesajlarında dosya yolları, kod satırları görünebilir
- ❌ Saldırganlar için bilgi toplama kolaylaşır

## 🔧 Hızlı Kontrol Komutu (Tek Satır)

```bash
cd /var/www/UniEduNote && source venv/bin/activate && python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DEBUG:', os.environ.get('DEBUG', 'Not Set'))"
```

## 📋 Kontrol Listesi

- [ ] `.env` dosyasında `DEBUG=False` var mı?
- [ ] Django settings'te `DEBUG=False` olarak ayarlanmış mı?
- [ ] Gunicorn yeniden başlatıldı mı?
- [ ] Web sitesinde detaylı hata mesajları görünmüyor mu?

## 🆘 Sorun Giderme

### Eğer DEBUG=False ama hala detaylı hatalar görüyorsanız:

1. **Cache temizle:**
```bash
python manage.py clear_cache
```

2. **Gunicorn loglarını kontrol et:**
```bash
journalctl -u gunicorn -n 50
```

3. **Settings.py'yi tekrar kontrol et:**
```bash
grep -n "DEBUG" uniedunote/settings.py
```

