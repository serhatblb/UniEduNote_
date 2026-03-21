# Gunicorn performans ayarları
# Kullanım: gunicorn -c gunicorn.conf.py uniedunote.wsgi:application

import multiprocessing

# CPU sayısına göre worker (2 CPU → 5 worker önerilir)
workers = multiprocessing.cpu_count() * 2 + 1

# Her worker'ın aynı anda handle edeceği bağlantı sayısı
worker_connections = 1000

# Timeout (saniye) — yavaş istekler için
timeout = 30

# Keep-alive: nginx → gunicorn bağlantısı açık kalsın
keepalive = 5

# Worker tipi: sync (varsayılan) - async için gevent kurulabilir
worker_class = "sync"

# Log seviyesi
loglevel = "warning"

# Graceful restart için max istek sayısı (memory leak önler)
max_requests = 1000
max_requests_jitter = 100
