# 🔐 CertWatch — Мониторинг SSL-сертификатов

CLI-инструмент для проверки срока действия SSL-сертификатов с поддержкой Docker и GitHub Container Registry.

## ✨ Возможности

- ✅ Проверка срока действия SSL-сертификатов
- 🎨 Красивый вывод в терминале (таблица с цветами)
- 🚨 Различает типы ошибок: просрочен, самоподписан, hostname mismatch
- 💾 Хранение списка доменов локально
- 🐳 Работа в Docker-контейнере
- 📦 Готовый образ в GHCR
- 📊 Exit-код для интеграции с CI/CD

## 🚀 Быстрый старт (из GHCR — рекомендуемый способ)

Не нужно ничего собирать — образ уже готов:

```bash
# Скачать образ
docker pull ghcr.io/ostenvrn/certwatch:latest

# Добавить домен
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest add github.com

# Проверить все домены
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest check

# Проверить один домен
docker run --rm ghcr.io/ostenvrn/certwatch:latest check google.com

    Важно: флаг -v "$PWD/data:/app/data" монтирует твою локальную папку data/ внутрь контейнера, чтобы список доменов сохранялся между запусками.

🐳 Локальная сборка (для разработки)
bash

# Сборка образа
docker build -t certwatch:latest .

# Запуск
docker run --rm -v "$PWD/data:/app/data" certwatch:latest check

🛠 Локальный запуск (Python)
bash

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Зависимости
pip install -r requirements.txt

# Использование
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

    Docker + Buildx — контейнеризация

    GitHub Actions — CI/CD

    GHCR — хранение образов

🔧 CI/CD

При каждом пуше в main GitHub Actions автоматически:

    Собирает Docker-образ

    Публикует его в ghcr.io/ostenvrn/certwatch

    Создаёт теги latest и main

📄 Лицензия

MIT
