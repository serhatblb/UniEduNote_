# 🎓 Akademik Hiyerarşi Sistemi - Kurulum ve Kullanım

## ✅ Tamamlanan Özellikler

### 1. Backend API'leri ✅
- `/api/academic/universities/` - Tüm üniversiteler
- `/api/academic/faculties/?university_id=X` - Fakülteler
- `/api/academic/departments/?faculty_id=X` - Bölümler
- `/api/academic/courses/?department_id=X` - Dersler
- `/api/academic/search/?q=query` - Text arama

### 2. Frontend Component ✅
- `AcademicHierarchySelector` - Reusable component
- Select2 entegrasyonu
- Zincir kontrolü (üst seçilmeden alt aktif değil)
- Lazy loading

### 3. Entegrasyon ✅
- Upload sayfası entegre edildi
- Filtreleme sayfası entegre edildi

### 4. Veri Yükleme Scripti ✅
- `load_30_universities.py` hazır

---

## 🚀 Kurulum Adımları

### 1. Veritabanına Veri Yükle

```bash
# Virtual environment'ı aktif et
source venv/bin/activate

# Veri yükleme scriptini çalıştır
python load_30_universites.py
```

**Beklenen Çıktı:**
```
🚀 30 Üniversite Verisi Yükleme Başladı...

✅ Üniversite oluşturuldu: İstanbul Üniversitesi
   → 3 fakülte, toplam 6 bölüm eklendi

...

🎉 Tüm üniversiteler başarıyla yüklendi!

📊 Özet:
   - Toplam Üniversite: 30
   - Toplam Fakülte: ~90
   - Toplam Bölüm: ~180
   - Toplam Ders: ~900
```

### 2. Cache Table Oluştur (Eğer yoksa)

```bash
python manage.py createcachetable
```

### 3. Migrate (Gerekirse)

```bash
python manage.py migrate
```

### 4. Static Dosyaları Topla

```bash
python manage.py collectstatic --noinput
```

### 5. Sunucuyu Yeniden Başlat

```bash
systemctl restart gunicorn
```

---

## 📋 Kullanım

### Upload Sayfası
1. Kullanıcı "Not Yükle" sayfasına gelir
2. Akademik hiyerarşi selector otomatik yüklenir
3. Üniversite seçilir → Fakülte aktif olur
4. Fakülte seçilir → Bölüm aktif olur
5. Bölüm seçilir → Ders aktif olur
6. Ders seçilir (ZORUNLU)
7. Form gönderilir

### Filtreleme Sayfası
1. Kullanıcı filtreleme alanına gelir
2. Akademik hiyerarşi selector yüklenir
3. Zincir kontrolü ile filtreleme yapılır
4. Text arama ile de filtreleme yapılabilir

---

## 🔧 Özelleştirme

### Component Kullanımı

```javascript
const selector = new AcademicHierarchySelector({
    container: '#my-container',
    onSelectionChange: (data) => {
        console.log(data);
        // {university_id, faculty_id, department_id, course_id}
    },
    required: ['university', 'faculty', 'department', 'course'],
    searchEnabled: true,
    apiBaseUrl: '/api/academic/'
});
```

### Public Methods

```javascript
// Seçili değerleri al
const selected = selector.getSelected();

// Geçerli mi kontrol et
const isValid = selector.isValid();

// Değerleri programatik olarak set et
selector.setValues(universityId, facultyId, departmentId, courseId);

// Sıfırla
selector.reset();
```

---

## 🐛 Sorun Giderme

### Component Yüklenmiyor
- jQuery ve Select2 yüklü mü kontrol et
- Browser console'da hata var mı kontrol et
- Static dosyalar toplanmış mı kontrol et

### API Çağrıları Çalışmıyor
- URL'ler doğru mu kontrol et (`/api/academic/`)
- Cache temizle: `python manage.py clear_cache`
- API endpoint'lerini test et: `curl http://localhost:8000/api/academic/universities/`

### Veri Görünmüyor
- Veri yükleme scripti çalıştırıldı mı?
- Veritabanında veri var mı kontrol et:
  ```python
  python manage.py shell
  >>> from categories.models import University
  >>> University.objects.count()
  ```

---

## 📊 Performans

- **Cache Süreleri:**
  - Üniversiteler: 1 saat
  - Fakülteler/Bölümler/Dersler: 30 dakika
  - Arama sonuçları: 15 dakika

- **Lazy Loading:**
  - Sadece gerektiğinde veri çekilir
  - Cache'den okunur mümkün olduğunca

---

## ✅ Test Senaryoları

1. ✅ Upload sayfasında zincir kontrolü
2. ✅ Filtreleme sayfasında zincir kontrolü
3. ✅ Text arama çalışıyor mu
4. ✅ Mobil uyumlu mu
5. ✅ Cache çalışıyor mu

---

## 🎯 Sonraki Adımlar

1. Daha fazla üniversite verisi ekle
2. Admin paneli ile veri yönetimi
3. Arama önerileri (autocomplete)
4. Popüler dersler gösterimi

