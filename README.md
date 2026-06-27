# Observability Stack

🇬🇧 [English](#english) | 🇹🇷 [Türkçe](#türkçe)

---

## English

Production-ready monitoring stack built on Prometheus + Grafana + Alertmanager, for any Docker-based application. Includes a sample microservices demo (Vertex) showing real application-level metrics and a live cascading-failure alert scenario.

### Setup

```bash
cp .env.example .env
openssl rand -base64 24        # paste the output into GF_ADMIN_PASSWORD in .env
docker compose up -d
```

Grafana: `http://localhost:3000` (credentials: see your `.env` file)
Prometheus targets: `http://localhost:9090/targets`

### Notification channels (Telegram + Email)

1. Copy `alertmanager/bot_token.example` → `alertmanager/bot_token`, paste your real Telegram bot token.
2. Copy `alertmanager/smtp_password.example` → `alertmanager/smtp_password`, paste your Gmail App Password (or other SMTP provider).
3. Edit `alertmanager/alertmanager.yml`, replacing the placeholders (`YOUR_GMAIL@gmail.com`, `123456789`, `RECIPIENT_EMAIL@gmail.com`) with real values.
4. `docker compose up -d --force-recreate alertmanager`

### Domain + HTTPS (Caddy)

This repo assumes Caddy is installed at the system level (not in Docker) and reverse-proxies your domain to Grafana:

```
your-domain.com {
    reverse_proxy 127.0.0.1:3000
}
```

Caddy automatically provisions and renews a Let's Encrypt certificate.

### Security

- Admin password comes from `.env`, never committed (`.gitignore`).
- Sign-up and anonymous access disabled.
- Prometheus / cAdvisor / node-exporter bound to `127.0.0.1` only — not exposed to the network.
- Grafana datasource provisioned automatically (no manual setup).
- All secrets (`bot_token`, `smtp_password`, `.env`, `alertmanager.yml.real`) are gitignored.

### Structure

- `prometheus/` — scrape config, `alerts/` alert rules (host + Vertex demo)
- `alertmanager/` — notification routing + clean Telegram/Email templates
- `grafana/provisioning/` — datasource + dashboards (auto-provisioned)
- `docs/runbook.md` — incident response runbook, linked directly from alert messages
- `vertex/` — sample 4-service microservices demo (gateway, checkout, inventory, notification) with built-in Prometheus instrumentation and a live latency-injection endpoint for demos

### Vertex demo services

| Service | Port (host) | Purpose |
|---|---|---|
| `gateway-service` | 8010 | Public entry point, generates synthetic traffic via `/demo/traffic` |
| `checkout-service` | 8011 | Orchestrates checkout: calls inventory + notification |
| `inventory-service` | 8012 | Stock lookup |
| `notification-service` | 8013 | Order confirmation; exposes `/admin/inject-latency` to simulate a degraded third-party provider live |

Demo flow: hit `/admin/inject-latency` on `notification-service` → watch latency cascade through checkout → gateway → alert fires (Telegram + Email) → clear with `/admin/clear-incident` → resolved notification arrives.

---

## Türkçe

Prometheus + Grafana + Alertmanager tabanlı, Docker'lı uygulamalar için hazır, production-ready izleme kurulumu. İçinde gerçekçi bir mikroservis demosu (Vertex) da var — uygulama seviyesi metrikler ve canlı bir "cascading failure" alarm senaryosu gösteriyor.

### Kurulum

```bash
cp .env.example .env
openssl rand -base64 24        # çıktıyı .env içindeki GF_ADMIN_PASSWORD'a yapıştır
docker compose up -d
```

Grafana: `http://localhost:3000` (kullanıcı/şifre: `.env` dosyasındaki değerler)
Prometheus hedefleri: `http://localhost:9090/targets`

### Bildirim kanalları (Telegram + Email)

1. `alertmanager/bot_token.example` → `alertmanager/bot_token` olarak kopyala, gerçek Telegram bot token'ını yapıştır.
2. `alertmanager/smtp_password.example` → `alertmanager/smtp_password` olarak kopyala, Gmail App Password'ünü (veya başka bir SMTP sağlayıcısının şifresini) yapıştır.
3. `alertmanager/alertmanager.yml`'i düzenle, placeholder'ları (`YOUR_GMAIL@gmail.com`, `123456789`, `RECIPIENT_EMAIL@gmail.com`) gerçek değerlerle değiştir.
4. `docker compose up -d --force-recreate alertmanager`

### Domain + HTTPS (Caddy)

Bu repo, Caddy'nin sistem seviyesinde (Docker dışında) kurulu olduğunu ve domaini Grafana'ya yönlendirdiğini varsayar:

```
sizin-domaininiz.com {
    reverse_proxy 127.0.0.1:3000
}
```

Caddy, Let's Encrypt sertifikasını otomatik alır ve yeniler.

### Güvenlik

- Admin şifresi `.env`'den gelir, repoya hiç girmez (`.gitignore`).
- Kayıt ve anonim erişim kapalı.
- Prometheus / cAdvisor / node-exporter sadece `127.0.0.1`'e açık — ağda görünmez.
- Grafana datasource'u otomatik bağlanır (manuel ekleme yok).
- Tüm sırlar (`bot_token`, `smtp_password`, `.env`, `alertmanager.yml.real`) gitignore'da.

### Yapı

- `prometheus/` — scrape config, `alerts/` alarm kuralları (host + Vertex demo)
- `alertmanager/` — bildirim yönlendirme + temiz Telegram/Email şablonları
- `grafana/provisioning/` — datasource + dashboard'lar (otomatik kurulu)
- `docs/runbook.md` — olay müdahale runbook'u, alarm mesajlarından doğrudan link
- `vertex/` — örnek 4 servisli mikroservis demosu (gateway, checkout, inventory, notification), hazır Prometheus instrumentation'ı ve canlı demo için gecikme enjeksiyonu endpoint'i ile

### Vertex demo servisleri

| Servis | Port (host) | Görevi |
|---|---|---|
| `gateway-service` | 8010 | Dış giriş noktası, `/demo/traffic` ile sentetik trafik üretir |
| `checkout-service` | 8011 | Checkout akışını yönetir: inventory + notification'ı çağırır |
| `inventory-service` | 8012 | Stok sorgusu |
| `notification-service` | 8013 | Sipariş onayı; `/admin/inject-latency` ile canlı olarak bir üçüncü parti sağlayıcının yavaşladığını simüle eder |

Demo akışı: `notification-service`'te `/admin/inject-latency`'e bas → gecikmenin checkout → gateway'e yayılışını izle → alarm düşer (Telegram + Email) → `/admin/clear-incident` ile temizle → resolved bildirimi gelir.