"""
Merkezi dosya güvenlik ayarları ve validasyon fonksiyonları
"""
import mimetypes
from django.core.exceptions import ValidationError

# Kabul edilebilir dosya türleri (uzantı -> MIME type mapping)
ALLOWED_FILE_TYPES = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'txt': 'text/plain',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'zip': 'application/zip',
    'rar': 'application/x-rar-compressed',
}

# Maksimum dosya boyutu (20 MB)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB in bytes

# İzin verilen uzantılar listesi
ALLOWED_EXTENSIONS = list(ALLOWED_FILE_TYPES.keys())


def validate_file_type(file):
    """
    Dosya türünü kontrol eder (uzantı ve MIME type)
    
    Args:
        file: Django UploadedFile objesi
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not file:
        return False, "Dosya seçilmedi."
    
    # 1. Dosya adı kontrolü
    if not file.name:
        return False, "Geçersiz dosya adı."
    
    # 2. Uzantı kontrolü
    ext = file.name.split('.')[-1].lower() if '.' in file.name else ''
    if not ext or ext not in ALLOWED_EXTENSIONS:
        allowed_str = ', '.join(ALLOWED_EXTENSIONS)
        return False, f"İzin verilmeyen dosya türü. İzin verilen türler: {allowed_str}"
    
    # 3. MIME type kontrolü (Python'un mimetypes modülü ile)
    file.seek(0)  # Dosya başına dön
    mime_type, _ = mimetypes.guess_type(file.name)
    
    # Eğer mimetypes tahmin edemezse, uzantıya göre kontrol et
    if not mime_type:
        mime_type = ALLOWED_FILE_TYPES.get(ext)
    
    # Beklenen MIME type ile karşılaştır
    expected_mime = ALLOWED_FILE_TYPES.get(ext)
    if mime_type and expected_mime and mime_type != expected_mime:
        # Bazı durumlarda esnek ol (örn: jpeg/jpg)
        if not (ext in ['jpg', 'jpeg'] and mime_type in ['image/jpeg', 'image/jpg']):
            return False, f"Dosya içeriği uzantı ile uyuşmuyor. Beklenen: {expected_mime}, Bulunan: {mime_type}"
    
    # 4. Dosya boyutu kontrolü
    if file.size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"Dosya boyutu {max_mb}MB'dan büyük olamaz."
    
    # 5. Dosya adı güvenliği (basit kontrol)
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '', file.name)
    if safe_name != file.name:
        return False, "Dosya adında özel karakter kullanılamaz."
    
    file.seek(0)  # Tekrar başa dön
    return True, ""


def get_file_validation_error(file):
    """
    Dosya validasyonu yapar ve hata mesajı döner
    
    Args:
        file: Django UploadedFile objesi
        
    Returns:
        str: Hata mesajı (boş string ise geçerli)
    """
    is_valid, error_message = validate_file_type(file)
    return error_message if not is_valid else ""

