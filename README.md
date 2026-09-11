🔐 CertWatch — Мониторинг SSL-сертификатов

CLI-инструмент для проверки срока действия SSL-сертификатов с поддержкой Docker и GitHub Container Registry.

✨ Возможности

- ✅ Проверка срока действия SSL-сертификатов
- 🎨 Красивый вывод в терминале (таблица с цветами)
- 🚨 Различает типы ошибок: просрочен, самоподписан, hostname mismatch
- 💾 Хранение списка доменов локально
- 🐳 Работа в Docker-контейнере
- 📦 Готовый образ в GHCR
- 📊 Exit-код для интеграции с CI/CD

🚀 Быстрый старт (из GHCR — рекомендуемый способ)

Не нужно ничего собирать — образ уже готов:

```bash

Скачать образ
docker pull ghcr.io/ostenvrn/certwatch:latest

Добавить домен
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest add github.com

Проверить все домены
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest check

Проверить один домен
docker run --rm ghcr.io/ostenvrn/certwatch:latest check google.com

    Важно: флаг -v "$PWD/data:/app/data" монтирует твою локальную папку data/ внутрь контейнера, чтобы список доменов сохранялся между запусками.

🐳 Локальная сборка (для разработки)

Сборка образа
docker build -t certwatch:latest .

Запуск
docker run --rm -v "$PWD/data:/app/data" certwatch:latest check

🛠 Локальный запуск 

Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

Зависимости
pip install -r requirements.txt

Использование
python3 src/certwatch.py add github.com
python3 src/certwatch.py check

📋 Команды
Команда	Что делает
add <домен>	Добавить домен в мониторинг
remove <домен>	Удалить домен
list	Показать список доменов
check	Проверить ВСЕ домены из списка
check <домен>	Проверить ОДИН домен без сохранения
🎯 Как это работает

CertWatch не сканирует всю систему и не ищет сертификаты автоматически.
Ты сам добавляешь домены в мониторинг, а потом проверяешь их.
Пошаговый пример
bash

1. Добавляем домены (можно добавлять сколько угодно)
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest add mysite.ru
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest add api.mysite.ru
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest add blog.mysite.ru

2. Смотрим список добавленных доменов
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest list

3. Проверяем ВСЕ домены из списка
docker run --rm -v "$PWD/data:/app/data" ghcr.io/ostenvrn/certwatch:latest check

4. Или проверяем ОДИН домен без сохранения в список
docker run --rm ghcr.io/ostenvrn/certwatch:latest check google.com

Где хранится список

Список доменов хранится в файле data/domains.txt на твоей машине
(он не попадает в Docker-образ и не публикуется в Git).

    Флаг -v "$PWD/data:/app/data" обязателен — он монтирует твою локальную папку внутрь контейнера,
    чтобы список сохранялся между запусками.
    Без него каждый запуск будет видеть пустой список.

📸 Пример вывода

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

❓ FAQ

Q: CertWatch проверит все мои сертификаты автоматически?
A: Нет. Ты сам добавляешь домены через add. Инструмент проверяет только то, что в списке.

Q: Что будет, если запустить check без -v?
A: Контейнер увидит пустой список и скажет 📭 Список доменов пуст. Флаг -v обязателен.

Q: Можно ли проверить домен, не добавляя его в список?
A: Да. Используй check <домен> — например, check google.com.

Q: Где хранится список доменов?
A: В файле data/domains.txt на твоей машине. Он не попадает в Git и не уходит в Docker-образ.

📄 Лицензия
MIT
