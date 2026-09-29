# ============================================
# COMMIT: refactor(docker): multi-stage build
# Дата: 2026-09-29
# Причина: единый этап сборки тащил в образ pip-кэш и компиляторы.
# Решение: builder-этап для зависимостей + чистый runtime-этап.
# Результат: меньше размер образа, меньше поверхности для атак.
# ============================================

# ============================================
# COMMIT: fix(security): run as non-root user
# Причина: контейнер запускался от root — замечание наставника.
# Решение: useradd appuser (UID 10001) + USER appuser перед ENTRYPOINT.
# Результат: whoami внутри контейнера = appuser.
# ============================================

# --- Этап 1: builder (зависимости) ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Сначала только requirements.txt — кэш работает
COPY requirements.txt .

# Ставим пакеты в ~/.local — потом скопируем в runtime
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Этап 2: runtime (финальный образ) ---
FROM python:3.12-slim

LABEL maintainer="Ostenvrn" \
      description="CertWatch — мониторинг SSL-сертификатов" \
      org.opencontainers.image.source="https://github.com/Ostenvrn/certwatch"

# Non-root пользователь
RUN useradd --create-home --uid 10001 --shell /bin/bash appuser

WORKDIR /app

# Копируем зависимости из builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Копируем код с владельцем appuser
COPY --chown=appuser:appuser src/ ./src/

# Папка для данных — сразу с владельцем
RUN mkdir -p /app/data && chown appuser:appuser /app/data

# Скрипт исполняемый
RUN chmod +x src/certwatch.py

# Переключаемся на non-root
USER appuser

# Точка входа
ENTRYPOINT ["python", "src/certwatch.py"]
CMD ["check"]
