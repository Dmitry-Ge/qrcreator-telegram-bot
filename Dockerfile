FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir aiogram qrcode[pil]

# Копируем файлы проекта
COPY . .

# Файл main.py запускается при старте контейнера
CMD ["python", "./main.py"]