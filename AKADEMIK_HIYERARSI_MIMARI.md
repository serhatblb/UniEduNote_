# 🎓 Akademik Hiyerarşi Sistemi - Mimari Tasarım

## 📊 Mevcut Durum Analizi

### ✅ Güçlü Yönler
1. **Model Yapısı:** Doğru hiyerarşi var (University → Faculty → Department → Course)
2. **AJAX Cascade:** Mevcut cascade yükleme çalışıyor
3. **Select2 Entegrasyonu:** Upload sayfasında Select2 kullanılıyor

### ❌ Sorunlar
1. **Zincir Kontrolü Eksik:** Üst seçilmeden alt seçilebiliyor
2. **Reusable Değil:** Filtreleme ve upload ayrı kodlar
3. **Text Arama Eksik:** Sadece dropdown, text arama yok
4. **Performans:** Her seçimde ayrı API çağrısı
5. **Veri Eksikliği:** 30 üniversite verisi yok

---

## 🏗️ Önerilen Mimari

### 1. Backend Yapısı

#### API Endpoint'leri (Yeni)
```
GET /api/academic/universities/          # Tüm üniversiteler (cache'li)
GET /api/academic/faculties/?university_id=X    # Üniversiteye göre fakülteler
GET /api/academic/departments/?faculty_id=X     # Fakülteye göre bölümler
GET /api/academic/courses/?department_id=X      # Bölüme göre dersler
GET /api/academic/search/?q=matematik           # Text arama (tüm seviyelerde)
```

#### Response Format (DTO)
```json
{
  "id": 1,
  "name": "İstanbul Üniversitesi",
  "code": "IU"  // Opsiyonel
}
```

#### Caching Stratejisi
- **Üniversiteler:** Cache'li (1 saat)
- **Fakülteler/Bölümler/Dersler:** Cache'li (30 dakika)
- **Text Arama:** Cache'li (15 dakika)

### 2. Frontend Yapısı

#### Reusable Component: `AcademicHierarchySelector`
```javascript
// Kullanım:
new AcademicHierarchySelector({
  container: '#filter-container',
  onSelectionChange: (data) => {
    // {university_id, faculty_id, department_id, course_id}
  },
  required: ['university', 'faculty', 'department', 'course'],
  searchEnabled: true
});
```

#### Özellikler:
- ✅ Zincir kontrolü (üst seçilmeden alt aktif değil)
- ✅ Dropdown + Text arama birleşimi
- ✅ Lazy loading (sadece gerektiğinde veri çek)
- ✅ Mobil uyumlu
- ✅ Select2 entegrasyonu

### 3. Veri Modeli

#### 30 Üniversite Listesi (Öncelikli)
1. İstanbul Üniversitesi
2. Ankara Üniversitesi
3. Boğaziçi Üniversitesi
4. Orta Doğu Teknik Üniversitesi (ODTÜ)
5. Hacettepe Üniversitesi
6. İstanbul Teknik Üniversitesi (İTÜ)
7. Galatasaray Üniversitesi
8. Koç Üniversitesi
9. Sabancı Üniversitesi
10. Bilkent Üniversitesi
11. Yıldız Teknik Üniversitesi
12. Marmara Üniversitesi
13. Ege Üniversitesi
14. Dokuz Eylül Üniversitesi
15. Gazi Üniversitesi
16. Anadolu Üniversitesi (AÖF)
17. Atatürk Üniversitesi
18. Erciyes Üniversitesi
19. Selçuk Üniversitesi
20. Akdeniz Üniversitesi
21. Çukurova Üniversitesi
22. Karadeniz Teknik Üniversitesi
23. Uludağ Üniversitesi
24. Trakya Üniversitesi
25. Ondokuz Mayıs Üniversitesi
26. İnönü Üniversitesi
27. Fırat Üniversitesi
28. Dicle Üniversitesi
29. Van Yüzüncü Yıl Üniversitesi
30. Kocaeli Üniversitesi

**Her üniversite için:**
- En az 3-5 fakülte
- Her fakülte için 2-4 bölüm
- Her bölüm için 5-10 ders

---

## 🔄 Akış Diyagramı

### Not Yükleme Akışı
```
1. Kullanıcı "Not Yükle" sayfasına gelir
2. Üniversite dropdown'u yüklenir (cache'den)
3. Kullanıcı üniversite seçer
   → Fakülte dropdown'u aktif olur
   → Fakülteler lazy load edilir
4. Kullanıcı fakülte seçer
   → Bölüm dropdown'u aktif olur
   → Bölümler lazy load edilir
5. Kullanıcı bölüm seçer
   → Ders dropdown'u aktif olur
   → Dersler lazy load edilir
6. Kullanıcı ders seçer (ZORUNLU)
7. Form gönderilir
```

### Filtreleme Akışı
```
1. Kullanıcı filtreleme alanına gelir
2. Tüm dropdown'lar başlangıçta disabled
3. Üniversite seçilir → Fakülte aktif
4. Fakülte seçilir → Bölüm aktif
5. Bölüm seçilir → Ders aktif
6. Text arama yapılabilir (her seviyede)
7. Filtreler uygulanır
```

---

## 💻 Teknik Detaylar

### Backend (Django)

#### 1. API Views (Yeni)
```python
# categories/views_api.py
class UniversityListView(APIView):
    @method_decorator(cache_page(60 * 60))  # 1 saat cache
    def get(self, request):
        universities = University.objects.all().order_by('name')
        return Response([{'id': u.id, 'name': u.name} for u in universities])

class FacultyListView(APIView):
    def get(self, request):
        university_id = request.GET.get('university_id')
        if not university_id:
            return Response([], status=400)
        faculties = Faculty.objects.filter(university_id=university_id)
        return Response([{'id': f.id, 'name': f.name} for f in faculties])
```

#### 2. Text Arama
```python
class AcademicSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response([])
        
        results = {
            'universities': University.objects.filter(name__icontains=query),
            'faculties': Faculty.objects.filter(name__icontains=query),
            'departments': Department.objects.filter(name__icontains=query),
            'courses': Course.objects.filter(name__icontains=query)
        }
        return Response(results)
```

### Frontend (JavaScript)

#### 1. Reusable Component
```javascript
class AcademicHierarchySelector {
    constructor(options) {
        this.container = options.container;
        this.onSelectionChange = options.onSelectionChange;
        this.required = options.required || [];
        this.searchEnabled = options.searchEnabled || true;
        
        this.init();
    }
    
    init() {
        // Select2 ile dropdown'ları oluştur
        // Event listener'ları ekle
        // Zincir kontrolü yap
    }
    
    loadData(level, parentId) {
        // Lazy loading
        // Cache kontrolü
        // API çağrısı
    }
    
    validateChain() {
        // Zincir kontrolü
        // Üst seçilmeden alt aktif değil
    }
}
```

---

## 📋 Implementation Planı

### Faz 1: Backend API'leri
1. ✅ API endpoint'leri oluştur
2. ✅ Caching ekle
3. ✅ Text arama endpoint'i

### Faz 2: Frontend Component
1. ✅ Reusable component oluştur
2. ✅ Select2 entegrasyonu
3. ✅ Zincir kontrolü
4. ✅ Text arama

### Faz 3: Entegrasyon
1. ✅ Upload sayfasına entegre et
2. ✅ Filtreleme sayfasına entegre et
3. ✅ Test et

### Faz 4: Veri Yükleme
1. ✅ 30 üniversite verisi
2. ✅ Fakülte/bölüm/ders verileri
3. ✅ Migration

---

## 🎯 Başarı Kriterleri

- ✅ Üst seçilmeden alt seçilemez
- ✅ Text arama çalışır
- ✅ Mobil uyumlu
- ✅ Performanslı (cache'li)
- ✅ Reusable (tek component)
- ✅ 30 üniversite verisi var

---

## 🚀 Sonraki Adımlar

1. Backend API'leri kodla
2. Frontend component'i kodla
3. Upload sayfasına entegre et
4. Filtreleme sayfasına entegre et
5. Veri yükleme script'i hazırla

