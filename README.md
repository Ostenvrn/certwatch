# 🔐 CertWatch — мониторинг SSL-сертификатов

[![CI](https://github.com/Ostenvrn/certwatch/actions/workflows/ci.yml/badge.svg)](https://github.com/Ostenvrn/certwatch/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![GHCR](https://img.shields.io/badge/ghcr.io-ostenvrn%2Fcertwatch-blue)](https://github.com/Ostenvrn/certwatch/pkgs/container/certwatch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CLI-инструмент для проверки срока действия SSL-сертификатов.
Работает в Docker, хранит список доменов локально, различает типы ошибок
(просрочен, самоподписан, hostname mismatch) и возвращает exit-код для CI/CD.

---

## ✨ Возможности

- ✅ Проверка срока действия SSL-сертификатов
- 🎨 Красивый вывод в терминале (таблица с цветами)
- 🚨 Различает типы ошибок: просрочен, самоподписан, hostname mismatch
- 💾 Локальное хранение списка доменов (volume)
- 🐳 Работа в Docker-контейнере (non-root, multi-stage build)
- 📦 Готовый образ в GHCR
- 📊 Exit-код для интеграции с CI/CD
- 🔒 Non-root пользователь внутри контейнера (UID 10001)

---

## 🚀 Быстрый старт

### Через Docker (рекомендуется)

Образ уже собран и опубликован в GHCR — собирать ничего не нужно.

```bash
# Скачать образ
docker pull ghcr.io/ostenvrn/certwatch:latest

# Добавить домен
docker run --rm -v "$PWD/data:/app/data" \
  ghcr.io/ostenvrn/certwatch:latest add github.com

# Проверить все домены
docker run --rm -v "$PWD/data:/app/data" \
  ghcr.io/ostenvrn/certwatch:latest check

# Проверить один домен, не добавляя в список
docker run --rm ghcr.io/ostenvrn/certwatch:latest check google.com
```

> **Важно:** флаг `-v "$PWD/data:/app/data"` монтирует твою локальную папку
> `data/` внутрь контейнера, чтобы список доменов сохранялся между запусками.
> Без него каждый запуск видит пустой список.

### Локально (для разработки)

```bash
# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Зависимости
pip install -r requirements.txt

# Использование
python3 src/certwatch.py add github.com
python3 src/certwatch.py check
```

---

## 📋 Команды

| Команда | Что делает |
|---------|-----------|
| `add <домен>` | Добавить домен в мониторинг |
| `remove <домен>` | Удалить домен из мониторинга |
| `list` | Показать список доменов |
| `check` | Проверить **все** домены из списка |
| `check <домен>` | Проверить **один** домен без сохранения |

---

## 📸 Пример вывода

```text
══════════════════════════════════════════════════════════════════════
📜 CERT WATCH — Статус SSL-сертификатов
══════════════════════════════════════════════════════════════════════

ДОМЕН                          СТАТУС          ИСТЕКАЕТ     ОСТАЛОСЬ
──────────────────────────────────────────────────────────────────────
github.com                     🟢 OK           2026-11-29   79 дн.
google.com                     🟢 OK           2026-11-02   51 дн.
expired.badssl.com             💀 ПРОСРОЧЕН    —            —
self-signed.badssl.com         🔓 САМОПОДПИСАН —            —

📊 ИТОГО:
  🟢 OK:            2
  💀 Просрочен:     1
  🔓 Самоподписан:  1
══════════════════════════════════════════════════════════════════════
```

---

## 🏗 Архитектура

```text
certwatch/
├── src/
│   ├── certwatch.py            # CLI: точка входа, argparse
│   ├── checkers/
│   │   └── ssl_checker.py      # проверка сертификата (ssl, socket)
│   ├── reporters/
│   │   └── console_report.py   # вывод таблицы (colorama, tabulate)
│   └── storage/
│       └── domain_store.py     # работа с data/domains.txt
├── data/
│   ├── domains.txt             # рабочий список (не в git)
│   └── domains.example.txt     # пример для новых пользователей
├── .github/workflows/ci.yml    # CI: lint → build → scan → push
├── Dockerfile                  # multi-stage build, non-root user
├── pyproject.toml              # конфиг ruff
└── requirements.txt
```

---

## 🛠 Разработка

```bash
# Установить dev-зависимости
pip install -r requirements.txt ruff

# Линтер
ruff check .

# Авто-фиксы
ruff check --fix .

# Форматирование
ruff format .

# Собрать образ локально
docker build -t certwatch:test .

# Проверить non-root
docker run --rm --entrypoint whoami certwatch:test
# → appuser
```

---

## 🔄 CI/CD

При каждом пуше в `main` GitHub Actions автоматически:

1. **Lint** — запускает `ruff check .`
2. **Build** — собирает Docker-образ (multi-stage, non-root)
3. **Scan** — проверяет образ на уязвимости через [Trivy](https://github.com/aquasecurity/trivy)
4. **Push** — публикует образ в [GHCR](https://github.com/Ostenvrn/certwatch/pkgs/container/certwatch)

Статус пайплайна — в бейдже вверху README.

---

## 🔧 Технологии

- **Python 3.12** — основной язык
- **ssl, socket** — проверка сертификатов
- **colorama, tabulate** — цветной вывод и таблицы
- **python-dateutil** — парсинг дат
- **Docker + Buildx** — контейнеризация, multi-stage build
- **GitHub Actions** — CI/CD
- **Trivy** — сканирование уязвимостей
- **GHCR** — хранение образов
- **ruff** — линтер и форматтер

---

## ❓ FAQ

**Q: CertWatch проверит все мои сертификаты автоматически?**
A: Нет. Ты сам добавляешь домены через `add`. Инструмент проверяет только то, что в списке.

**Q: Что будет, если запустить `check` без `-v`?**
A: Контейнер увидит пустой список и скажет `📭 Список доменов пуст`. Флаг `-v` обязателен.

**Q: Можно ли проверить домен, не добавляя его в список?**
A: Да. Используй `check <домен>` — например, `check google.com`.

**Q: Где хранится список доменов?**
A: В файле `data/domains.txt` на твоей машине. Он не попадает в Git и не уходит в Docker-образ.

**Q: Почему контейнер запускается не от root?**
A: Это требование безопасности. Если злоумышленник найдёт уязвимость в приложении,
он не получит root внутри контейнера и не сможет выйти за его пределы (CVE-2019-5736).

---

## 📄 Лицензия

MIT — используй, форкай, делай что хочешь.
