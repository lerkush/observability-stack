# Runbook

Alarm düştüğünde ne yapılacağı. Telegram mesajındaki link doğrudan ilgili bölüme gelir.

## instance-down
**Belirti:** Bir hedef 1 dakikadır yanıt vermiyor (`up == 0`).
**Kontrol:** Servis ayakta mı? `docker compose ps`, `docker compose logs <servis>`.
**Çözüm:** `docker compose restart <servis>`. Düzelmiyorsa loglara ve kaynaklara (RAM/disk) bak.

## cpu-high
**Belirti:** CPU 5 dakikadır %90 üstünde.
**Kontrol:** Hangi process/container? `docker stats`, `top`.
**Çözüm:** Kaçak process'i durdur, ölçekle ya da kaynak limiti ekle. Trafik artışıysa kapasite planla.

## memory-high
**Belirti:** RAM kullanımı %90 üstünde.
**Kontrol:** `docker stats` ile hangi container?
**Çözüm:** Memory leak şüphesi varsa restart; kalıcıysa limit ayarla veya RAM artır.

## disk-low
**Belirti:** Disk %85 üstünde dolu.
**Kontrol:** `df -h`, büyük dosyalar: `du -sh /* 2>/dev/null | sort -h`.
**Çözüm:** Eski log/imajları temizle: `docker system prune`. Kalıcıysa diski büyüt.
