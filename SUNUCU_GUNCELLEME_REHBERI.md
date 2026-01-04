# 🔄 Sunucu Settings.py Güncelleme Rehberi

## 📋 Yapılacaklar

### 1. Settings.py Dosyasını Güncelle

Sunucudaki `uniedunote/settings.py` dosyasını yeni versiyonla değiştir.

**Değişiklikler:**
- ✅ SECRET_KEY güvenliği artırıldı (fallback var ama uyarı veriyor)
- ✅ DEBUG production-safe hale getirildi
- ✅ ALLOWED_HOSTS daha akıllı yapılandırma
- ✅ CSRF_TRUSTED_ORIGINS otomatik yapılandırma
- ✅ Security headers eklendi (HTTPS, XSS, CSRF koruması)

### 2. .env Dosyası Kontrolü

`.env` dosyasında şu değişkenlerin olduğundan emin ol:

```bash
# ZORUNLU (Production için)
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=dersnotlarım.com.tr,www.dersnotlarım.com.tr
BACKEND_BASE_URL=https://dersnotlarım.com.tr

# Opsiyonel (E-posta için)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=UniEduNote <your-email@gmail.com>
SENDGRID_API_KEY=your-sendgrid-api-key
```

### 3. Deploy Adımları

```bash
# 1. Git pull yap
git pull origin main

# 2. Migration'ları çalıştır (eğer yeni migration varsa)
python manage.py migrate

# 3. Static files topla
python manage.py collectstatic --noinput

# 4. Cache table oluştur (eğer yoksa)
python manage.py createcachetable

# 5. Sunucuyu yeniden başlat
# (Render/Heroku için otomatik, VPS için: systemctl restart gunicorn)
```

## ⚠️ Önemli Notlar

### SECRET_KEY
- Eğer `.env` dosyasında `SECRET_KEY` yoksa, uyarı verir ama çalışmaya devam eder
- **Production'da mutlaka ayarlanmalı!**

### DEBUG
- `.env` dosyasında `DEBUG=False` olmalı
- Eğer yoksa otomatik olarak `False` olur (güvenli)

### ALLOWED_HOSTS
- `.env` dosyasında domain adları olmalı
- Eğer yoksa ve `DEBUG=False` ise, tüm host'lara izin verir (GÜVENLİK RİSKİ!)
- **Production'da mutlaka ayarlanmalı!**

### CSRF_TRUSTED_ORIGINS
- Otomatik olarak `ALLOWED_HOSTS`'den oluşturulur
- Eski `dersnotlarım.com.tr` kontrolü de korundu (geriye dönük uyumluluk)

## 🔍 Değişiklik Detayları

### Önceki Kod:
```python
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-varsayilan-anahtar")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
```

### Yeni Kod:
```python
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    warnings.warn("SECRET_KEY ayarlanmamış!")
    SECRET_KEY = "django-insecure-temporary-key-change-in-production"

DEBUG_ENV = os.environ.get("DEBUG", "False").lower()
DEBUG = DEBUG_ENV in ("true", "1", "yes")

ALLOWED_HOSTS_ENV = os.environ.get("ALLOWED_HOSTS", "")
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(",") if host.strip()]
else:
    if DEBUG:
        ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    else:
        ALLOWED_HOSTS = ["*"]  # Uyarı ile
```

### Eklenen Security Headers:
```python
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True  # Production'da
SECURE_HSTS_SECONDS = 31536000
```

## ✅ Test Checklist

Güncellemeden sonra kontrol et:

- [ ] Site açılıyor mu?
- [ ] Login çalışıyor mu?
- [ ] Not listesi görüntüleniyor mu?
- [ ] HTTPS yönlendirmesi çalışıyor mu? (production'da)
- [ ] Console'da uyarı var mı? (SECRET_KEY, ALLOWED_HOSTS)

## 🚨 Sorun Giderme

### "SECRET_KEY ayarlanmamış" uyarısı
- `.env` dosyasına `SECRET_KEY=...` ekle
- Sunucuyu yeniden başlat

### "ALLOWED_HOSTS ayarlanmamış" uyarısı
- `.env` dosyasına `ALLOWED_HOSTS=yourdomain.com` ekle
- Sunucuyu yeniden başlat

### CSRF hatası
- `CSRF_TRUSTED_ORIGINS` otomatik oluşturulur
- Eğer sorun devam ederse, `.env`'e manuel ekle:
  ```
  CSRF_TRUSTED_ORIGINS=https://dersnotlarım.com.tr,https://www.dersnotlarım.com.tr
  ```

### HTTPS yönlendirmesi çalışmıyor
- `DEBUG=False` olduğundan emin ol
- Reverse proxy (nginx) yapılandırmasını kontrol et

