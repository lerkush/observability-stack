# Observability Stack

Prometheus + Grafana + Alertmanager tabanlı, Docker'lı uygulamalar için hazır izleme kurulumu.

## Kurulum

```bash
cp .env.example .env
openssl rand -base64 24        # çıktıyı .env içindeki GF_ADMIN_PASSWORD'a yapıştır
docker compose up -d
```

Grafana: http://localhost:3000  (kullanıcı/şifre: .env dosyasındaki değerler)
Prometheus hedefleri: http://localhost:9090/targets

## Güvenlik

- Admin şifresi `.env`'den gelir, repoya girmez (`.gitignore`).
- Kayıt ve anonim erişim kapalı.
- Prometheus / cAdvisor / node-exporter sadece `127.0.0.1`'e açık — ağda görünmez.
- Grafana datasource'u otomatik bağlanır (manuel ekleme yok).

## Yapı

- `prometheus/` — scrape config, `alerts/` alarm kuralları (Adım 3)
- `alertmanager/` — bildirim yönlendirme + temiz şablonlar (Adım 3)
- `grafana/provisioning/` — datasource + dashboard'lar (Adım 2'de JSON eklenir)
- `docs/runbook.md` — Pro paket runbook'u (Adım 5)
- `app/` — örnek FastAPI instrumentation (Adım 4)
