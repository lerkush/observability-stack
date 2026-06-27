# Runbook

🇬🇧 [English](#english) | 🇹🇷 [Türkçe](#türkçe)

What to do when an alert fires. The link in each Telegram/Email alert message points directly to the matching section below.

---

## English

### instance-down
**Symptom:** A target has not responded for 1 minute (`up == 0`).
**Check:** Is the service running? `docker compose ps`, `docker compose logs <service>`.
**Fix:** `docker compose restart <service>`. If it persists, check logs and resource usage (RAM/disk).

### cpu-high
**Symptom:** CPU has been above 90% for 5 minutes.
**Check:** Which process/container? `docker stats`, `top`.
**Fix:** Stop the runaway process, scale, or add a resource limit. If it's traffic-driven, plan capacity.

### memory-high
**Symptom:** RAM usage above 90%.
**Check:** `docker stats` — which container?
**Fix:** Restart if a memory leak is suspected; otherwise set a limit or add RAM.

### disk-low
**Symptom:** Disk usage above 85%.
**Check:** `df -h`, find large files: `du -sh /* 2>/dev/null | sort -h`.
**Fix:** Clean old logs/images: `docker system prune`. If persistent, grow the disk.

### notification-latency
**Symptom:** notification-service's p95 response time exceeded 1 second.
**Check:** Is `/admin/inject-latency` an active demo simulation, or is this real? `docker logs notification-service --tail 50`.
**Fix:** If it's a demo, clear it with `/admin/clear-incident`. If it's real, check the status of the third-party email/SMS provider this service depends on.

### checkout-errors
**Symptom:** checkout-service's 5xx error rate exceeded 10%.
**Check:** `docker logs checkout-service --tail 50`. Which downstream service (inventory or notification) is causing errors/timeouts?
**Fix:** Restart the failing downstream service (`docker compose restart <service>`). If it's notification-service, try `/admin/clear-incident`. If it persists, check that service's own logs.

---

## Türkçe

### instance-down
**Belirti:** Bir hedef 1 dakikadır yanıt vermiyor (`up == 0`).
**Kontrol:** Servis ayakta mı? `docker compose ps`, `docker compose logs <servis>`.
**Çözüm:** `docker compose restart <servis>`. Düzelmiyorsa loglara ve kaynaklara (RAM/disk) bak.

### cpu-high
**Belirti:** CPU 5 dakikadır %90 üstünde.
**Kontrol:** Hangi process/container? `docker stats`, `top`.
**Çözüm:** Kaçak process'i durdur, ölçekle ya da kaynak limiti ekle. Trafik artışıysa kapasite planla.

### memory-high
**Belirti:** RAM kullanımı %90 üstünde.
**Kontrol:** `docker stats` ile hangi container?
**Çözüm:** Memory leak şüphesi varsa restart; kalıcıysa limit ayarla veya RAM artır.

### disk-low
**Belirti:** Disk %85 üstünde dolu.
**Kontrol:** `df -h`, büyük dosyalar: `du -sh /* 2>/dev/null | sort -h`.
**Çözüm:** Eski log/imajları temizle: `docker system prune`. Kalıcıysa diski büyüt.

### notification-latency
**Belirti:** notification-service'in p95 yanıt süresi 1 saniyeyi geçti.
**Kontrol:** `/admin/inject-latency` ile kasıtlı bir incident simülasyonu mu aktif, yoksa gerçek bir yavaşlama mı? `docker logs notification-service --tail 50`.
**Çözüm:** Eğer demo/test amaçlıysa `/admin/clear-incident` ile temizle. Gerçek bir yavaşlamaysa, servisin bağlı olduğu üçüncü parti sağlayıcının (email/SMS) durumunu kontrol et.

### checkout-errors
**Belirti:** checkout-service'te 5xx hata oranı %10'u geçti.
**Kontrol:** `docker logs checkout-service --tail 50`. Hangi downstream servis (inventory veya notification) hataya/timeout'a sebep oluyor?
**Çözüm:** Sorunlu downstream servisi yeniden başlat (`docker compose restart <servis>`). Sorun notification-service'teyse `/admin/clear-incident` dene. Düzelmiyorsa downstream servisin loglarına bak.