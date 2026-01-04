# Git Pull Sorunu Çözüm Rehberi

## Sorun
`git pull` yaparken `staticfiles/` klasöründeki dosyalar çakışıyor.

## Neden?
`staticfiles/` klasörü git'te takip ediliyor ama bu klasör `collectstatic` komutu ile oluşturulur ve git'te olmamalı.

## Çözüm

### Adım 1: Local'de .gitignore Güncelle (✅ YAPILDI)
`.gitignore` dosyasına `staticfiles/` eklendi.

### Adım 2: Local'de Migration Commit Et
```bash
# Local'de (development)
git add .gitignore
git add rewards/migrations/
git commit -m "Gamification sistemi eklendi, staticfiles gitignore'a eklendi"
git push
```

### Adım 3: Sunucuda Staticfiles'i Git'ten Kaldır
```bash
# Sunucuda
cd /var/www/UniEduNote

# Staticfiles klasörünü git'ten kaldır (dosyaları silmez, sadece git takibinden çıkarır)
git rm -r --cached staticfiles/

# Commit et (local'de yapılacak, sunucuda sadece pull yapılacak)
# VEYA sunucuda geçici çözüm:
rm -rf staticfiles/
```

### Adım 4: Sunucuda Pull Yap
```bash
# Sunucuda
cd /var/www/UniEduNote
source venv/bin/activate

# Önce staticfiles'i sil (git pull'dan önce)
rm -rf staticfiles/

# Pull yap
git pull

# Migrations uygula
python manage.py migrate rewards

# Static dosyaları yeniden topla
python manage.py collectstatic --noinput

# Web sunucusunu restart et
sudo systemctl restart gunicorn
```

## Alternatif Çözüm (Daha Güvenli)

Eğer staticfiles klasörünü silmek istemiyorsanız:

```bash
# Sunucuda
cd /var/www/UniEduNote

# Mevcut değişiklikleri stash'le
git stash

# Pull yap
git pull

# Stash'i geri getir (gerekirse)
# git stash pop

# Migrations uygula
python manage.py migrate rewards

# Static dosyaları yeniden topla
python manage.py collectstatic --noinput
```

## Önemli Notlar

1. **staticfiles/ klasörü git'te olmamalı** - Bu klasör `collectstatic` ile oluşturulur
2. **Her sunucuda collectstatic çalıştırılmalı** - Static dosyalar sunucuya özeldir
3. **.gitignore güncellendi** - Artık staticfiles git'te takip edilmeyecek

## Kontrol

Pull'dan sonra:
```bash
# Migrations uygulandı mı?
python manage.py showmigrations rewards

# Static dosyalar var mı?
ls -la staticfiles/css/theme.css

# Her şey tamam!
```

