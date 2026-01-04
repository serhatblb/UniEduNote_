# 🚨 Sunucuda Git Pull Sorunu - HIZLI ÇÖZÜM

## Sorun
`git pull` yaparken `staticfiles/` klasörü çakışıyor.

## ⚡ HIZLI ÇÖZÜM (Sunucuda)

```bash
# 1. Staticfiles klasörünü sil (collectstatic ile yeniden oluşturulacak)
rm -rf staticfiles/

# 2. Pull yap
git pull

# 3. Migrations uygula
python manage.py migrate rewards

# 4. Static dosyaları topla
python manage.py collectstatic --noinput

# 5. Web sunucusunu restart et
sudo systemctl restart gunicorn
```

## ✅ TAMAM! Artık çalışmalı.

---

## 📝 Detaylı Açıklama

### Neden Bu Sorun Oluştu?
- `staticfiles/` klasörü git'te takip ediliyordu
- Bu klasör `collectstatic` ile oluşturulur ve git'te olmamalı
- `.gitignore` dosyasına `staticfiles/` eklendi (local'de)

### Neden Staticfiles'i Silebiliriz?
- `staticfiles/` klasörü her zaman `collectstatic` ile yeniden oluşturulabilir
- Kaynak dosyalar `static/` klasöründe (git'te)
- Sunucuda her pull'dan sonra `collectstatic` çalıştırılmalı

### Sonraki Pull'larda
Artık `.gitignore` güncellendiği için `staticfiles/` git'te takip edilmeyecek ve bu sorun tekrar olmayacak.

