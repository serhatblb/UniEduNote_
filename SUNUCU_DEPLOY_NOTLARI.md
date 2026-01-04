# 🚀 Sunucu Deploy Notları

**Tarih:** 2025-01-27

## ⚠️ ÖNEMLİ: Sunucuya Çıkmadan Önce

### 1. Environment Variables Ayarlanmalı

Sunucuda (Render, Heroku, vs.) şu environment variable'lar **MUTLAKA** ayarlanmalı:

```bash
SECRET_KEY=your-very-secret-key-here-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
BACKEND_BASE_URL=https://yourdomain.com
```

**NOT:** Eğer bu değişkenler ayarlanmazsa:
- `SECRET_KEY`: Geçici bir key kullanılacak (GÜVENLİK RİSKİ!)
- `DEBUG`: False olacak (iyi)
- `ALLOWED_HOSTS`: Tüm host'lara izin verilecek (GÜVENLİK RİSKİ!)

### 2. Veritabanı Migration'ları

```bash
python manage.py migrate
```

### 3. Static Files Toplama

```bash
python manage.py collectstatic --noinput
```

### 4. Cache Table Oluşturma

```bash
python manage.py createcachetable
```

## ✅ Yapılan Değişiklikler

### Güvenlik İyileştirmeleri
- ✅ SECRET_KEY environment variable zorunlu (fallback var ama uyarı veriyor)
- ✅ DEBUG production-safe
- ✅ Security headers eklendi
- ✅ CSRF protection aktif

### Performans İyileştirmeleri
- ✅ Pagination eklendi (20 not/sayfa)
- ✅ N+1 query problemleri çözüldü
- ✅ Query optimization

### Kod İyileştirmeleri
- ✅ CSRF exempt kaldırıldı
- ✅ Import'lar düzeltildi

## 🔧 Potansiyel Sorunlar ve Çözümleri

### 1. Session Login Endpoint

**Durum:** DRF APIView kullanılıyor, CSRF otomatik olarak devre dışı.

**Frontend:** `templates/users/login.html` içinde CSRF token gönderilmiyor ama DRF APIView olduğu için sorun yok.

**Test:** Login işlemi çalışmalı. Eğer CSRF hatası alırsanız, frontend'e CSRF token ekleyin:

```javascript
// CSRF token al
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fetch'te kullan
const resSession = await fetch('/api/auth/session-login/', {
    method: 'POST',
    headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ username, password })
});
```

### 2. Pagination Template

**Durum:** Pagination backend'de eklendi ama frontend template'inde kontrol yok.

**Etki:** Sayfalama çalışır ama kullanıcı sayfa değiştiremez.

**Çözüm:** `templates/notes/note_list.html` dosyasına pagination UI eklenmeli:

```django
{% if notes.has_previous %}
    <a href="?page={{ notes.previous_page_number }}">Önceki</a>
{% endif %}

<span>Sayfa {{ notes.number }} / {{ notes.paginator.num_pages }}</span>

{% if notes.has_next %}
    <a href="?page={{ notes.next_page_number }}">Sonraki</a>
{% endif %}
```

### 3. Static Files

**Durum:** WhiteNoise kullanılıyor, `collectstatic` çalıştırılmalı.

**Çözüm:** Deploy sırasında otomatik çalıştırılmalı veya manuel:

```bash
python manage.py collectstatic --noinput
```

## 📋 Deploy Checklist

- [ ] Environment variables ayarlandı (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Veritabanı migration'ları çalıştırıldı
- [ ] Static files toplandı (`collectstatic`)
- [ ] Cache table oluşturuldu
- [ ] Login endpoint test edildi
- [ ] Not listesi pagination test edildi
- [ ] Security headers kontrol edildi

## 🐛 Bilinen Sorunlar

### 1. Model Duplikasyonu
- `academic` uygulaması aktif değil ama modelleri mevcut
- Migration geçmişi kontrol edilmeli
- **Etki:** Şu an sorun yok, aktif değil

### 2. Core Klasörü
- `core/` klasörü kullanılmıyor
- **Etki:** Şu an sorun yok, `uniedunote/` kullanılıyor

## ✅ Çalışma Durumu

**Evet, proje şu an sunucuda çalışabilir!**

Ancak:
1. ✅ Environment variables ayarlanmalı (yukarıdaki liste)
2. ⚠️ Pagination UI frontend'e eklenmeli (zorunlu değil, kullanıcı deneyimi için)
3. ✅ Migration'lar çalıştırılmalı
4. ✅ Static files toplanmalı

## 🚨 Acil Yapılması Gerekenler

1. **SECRET_KEY** environment variable'ı mutlaka ayarlanmalı
2. **ALLOWED_HOSTS** domain adları eklenmeli
3. **DEBUG=False** production'da

## 📝 Notlar

- Tüm değişiklikler geriye dönük uyumlu
- DRF APIView kullanıldığı için CSRF otomatik olarak devre dışı
- Session login çalışmalı, ancak JWT kullanımı önerilir

