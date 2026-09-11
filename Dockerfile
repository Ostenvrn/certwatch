# Легковесный базовый образ Python
FROM python:3.12-slim

# Метаданные
LABEL maintainer="Ostenvrn"
LABEL description="CertWatch — мониторинг SSL-сертификатов"

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем только requirements — так Docker кэширует слои
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY src/ ./src/

# Создаём папку для данных (volume подмонтируется сюда)
RUN mkdir -p /app/data

# Делаем скрипт исполняемым
RUN chmod +x src/certwatch.py

# Точка входа: запускаем certwatch
ENTRYPOINT ["python3", "src/certwatch.py"]

# По умолчанию — команда check
CMD ["check"]
