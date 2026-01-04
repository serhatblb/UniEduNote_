# Sunucuda Static Dosyalar (CSS) Sorunu - Adım Adım Çözüm

## Sorun: Permission Denied

`venv/bin/activate` dosyasını doğrudan çalıştırmaya çalışıyorsunuz. Bu dosya `source` komutu ile çalıştırılmalı.

## ✅ DOĞRU KULLANIM

### Adım 1: Virtual Environment'ı Aktif Et
```bash
# DOĞRU:
source venv/bin/activate

# VEYA kısa versiyonu:
. venv/bin/activate
```

**NOT:** `source` veya `.` komutunu kullanmadan `venv/bin/activate` yazarsanız "Permission denied" hatası alırsınız.

### Adım 2: Aktif Olduğunu Kontrol Et
Virtual environment aktif olduğunda prompt'unuz şöyle görünür:
```bash
(venv) root@uniedunote-server:/var/www/UniEduNote#
```

### Adım 3: Static Dosyaları Topla
```bash
python manage.py collectstatic --noinput
```

### Adım 4: Web Sunucusunu Yeniden Başlat
```bash
# Gunicorn kullanıyorsanız:
sudo systemctl restart gunicorn

# VEYA servisinizin adı ne ise:
sudo systemctl restart your-service-name

# Nginx'i de yeniden yükleyin (genellikle gerekmez):
sudo systemctl reload nginx
```

## 🔍 Eğer Hala Permission Denied Alıyorsanız

### Dosya İzinlerini Kontrol Et
```bash
ls -la venv/bin/activate
```

### İzinleri Düzelt (Gerekirse)
```bash
chmod +x venv/bin/activate
```

### Virtual Environment'ın Varlığını Kontrol Et
```bash
ls -la venv/bin/
```

Eğer `venv` klasörü yoksa veya bozuksa, yeniden oluşturmanız gerekebilir:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📋 TAM KOMUT SETİ (Kopyala-Yapıştır)

```bash
# 1. Proje dizinine git
cd /var/www/UniEduNote

# 2. Virtual environment'ı aktif et
source venv/bin/activate

# 3. Static dosyaları topla
python manage.py collectstatic --noinput

# 4. Web sunucusunu yeniden başlat
sudo systemctl restart gunicorn

# 5. Kontrol et
ls -la staticfiles/css/
```

## 🎯 Hızlı Test

Static dosyaların yüklendiğini kontrol etmek için:
```bash
# Static dosyaların varlığını kontrol et
ls -la staticfiles/css/theme.css
ls -la staticfiles/css/style.css

# Dosyalar görünüyorsa ✅ başarılı!
```

## ⚠️ Önemli Notlar

1. **Her zaman `source` kullanın:** `source venv/bin/activate` veya `. venv/bin/activate`
2. **Root kullanıcısı olarak çalışıyorsanız:** `sudo` gerekmez, direkt komutları çalıştırabilirsiniz
3. **Her kod değişikliğinden sonra:** `collectstatic` çalıştırın
4. **Production'da:** `DEBUG=False` olmalı ve WhiteNoise kullanılmalı

## 🐛 Sorun Giderme

### Sorun: "python: command not found"
```bash
# Python3 kullanın:
python3 manage.py collectstatic --noinput
```

### Sorun: "No module named django"
```bash
# Virtual environment aktif mi kontrol edin
# Aktif değilse:
source venv/bin/activate

# Requirements'ları yükleyin:
pip install -r requirements.txt
```

### Sorun: "staticfiles klasörü yok"
```bash
# Klasörü oluşturun:
mkdir -p staticfiles

# Sonra collectstatic çalıştırın:
python manage.py collectstatic --noinput
```

