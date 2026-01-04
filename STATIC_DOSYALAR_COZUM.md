# Static Dosyalar (CSS) Sorunu Çözüm Rehberi

## Sorun
CSS dosyaları sayfalarda görünmüyor veya çalışmıyor.

## Çözüm

### 1. Local (Geliştirme Ortamı) - ✅ TAMAMLANDI
```bash
# Virtual environment'ı aktif et
source venv/bin/activate

# Static dosyaları topla
python manage.py collectstatic --noinput
```

### 2. Sunucu (Production) - YAPILMASI GEREKENLER

#### Adım 1: Sunucuya SSH ile bağlan
```bash
ssh kullanici@sunucu-ip
```

#### Adım 2: Proje dizinine git
```bash
cd /path/to/UniEduNote_
```

#### Adım 3: Virtual environment'ı aktif et
```bash
source venv/bin/activate
# veya
source .venv/bin/activate
# veya projenizdeki virtual environment yoluna göre
```

#### Adım 4: Static dosyaları topla
```bash
python manage.py collectstatic --noinput
```

#### Adım 5: Web sunucusunu yeniden başlat
```bash
# Gunicorn kullanıyorsanız
sudo systemctl restart gunicorn
# veya
sudo systemctl restart your-service-name

# Nginx kullanıyorsanız (genellikle gerekmez ama kontrol edin)
sudo systemctl reload nginx
```

## Kontrol

### Static dosyaların doğru yüklendiğini kontrol et:
1. Tarayıcıda sayfayı aç
2. F12 (Developer Tools) aç
3. Network sekmesine git
4. Sayfayı yenile (F5)
5. `theme.css` veya `style.css` dosyasının yüklendiğini kontrol et

### Eğer hala çalışmıyorsa:

#### 1. STATIC_ROOT kontrolü
`settings.py` dosyasında şu satırlar olmalı:
```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

#### 2. WhiteNoise kontrolü
`settings.py` dosyasında şu ayarlar olmalı:
```python
MIDDLEWARE = [
    # ...
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

#### 3. URL yapılandırması kontrolü
`urls.py` dosyasında (ana urls.py) şu satırlar olmalı:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... diğer URL'ler
]

# Development için static dosyaları serve et
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 4. Template'lerde static tag kontrolü
Tüm template dosyalarının başında şu satır olmalı:
```django
{% load static %}
```

Ve CSS dosyaları şu şekilde yüklenmeli:
```django
<link rel="stylesheet" href="{% static 'css/theme.css' %}">
```

## Hızlı Test

Sunucuda şu komutu çalıştırarak static dosyaların varlığını kontrol edin:
```bash
ls -la staticfiles/css/
```

Şu dosyalar görünmeli:
- `theme.css`
- `style.css`

## Önemli Notlar

1. **Her kod değişikliğinden sonra** `collectstatic` çalıştırılmalı
2. **Production'da** `DEBUG=False` olmalı ve WhiteNoise kullanılmalı
3. **Static dosyalar** `staticfiles/` klasöründe toplanır (git'e eklenmemeli)
4. **Kaynak dosyalar** `static/` klasöründe kalır (git'e eklenmeli)

## Otomatikleştirme (Opsiyonel)

Sunucuda her pull'dan sonra otomatik çalışması için bir script oluşturabilirsiniz:

`deploy.sh`:
```bash
#!/bin/bash
cd /path/to/UniEduNote_
source venv/bin/activate
git pull
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart gunicorn
```

Çalıştırılabilir yapın:
```bash
chmod +x deploy.sh
```

Kullanım:
```bash
./deploy.sh
```

