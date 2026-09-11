# 🔐 CertWatch — Мониторинг SSL-сертификатов

CLI-инструмент для проверки срока действия SSL-сертификатов с поддержкой Docker.

## ✨ Возможности

- ✅ Проверка срока действия SSL-сертификатов
- 🎨 Красивый вывод в терминале (таблица с цветами)
- 🚨 Различает типы ошибок: просрочен, самоподписан, hostname mismatch
- 💾 Хранение списка доменов локально
- 🐳 Работа в Docker-контейнере
- 📊 Exit-код для интеграции с CI/CD

## 🚀 Быстрый старт (Docker)

```bash
# Сборка образа
docker build -t certwatch .

# Добавление домена
docker run --rm -v "$PWD/data:/app/data" certwatch add github.com

# Проверка всех доменов
docker run --rm -v "$PWD/data:/app/data" certwatch check

🛠 Локальный запуск (Python)
bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 src/certwatch.py add github.com
python3 src/certwatch.py check

📋 Команды
Команда	Что делает
add <домен>	Добавить домен в мониторинг
remove <домен>	Удалить домен
list	Показать список доменов
check	Проверить все домены
check <домен>	Проверить один домен
📸 Пример вывода
text

══════════════════════════════════════════════════════════════════════
📜 CERT WATCH — Статус SSL-сертификатов
══════════════════════════════════════════════════════════════════════

ДОМЕН                          СТАТУС          ИСТЕКАЕТ     ОСТАЛОСЬ
──────────────────────────────────────────────────────────────────────
github.com                     🟢 OK           2026-11-29   79 дн.
google.com                     🟢 OK           2026-11-02   51 дн.
expired.badssl.com             💀 ПРОСРОЧЕН    —            —
self-signed.badssl.com         🔓 САМОПОДПИСАН —            —

🧰 Технологии

    Python 3.12

    ssl, socket — проверка сертификатов

    colorama — цветной вывод

    python-dateutil — парсинг дат

    Docker — контейнеризация
