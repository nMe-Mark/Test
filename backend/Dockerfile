
# Dockerfile за Flask backend
FROM python:3.11-slim

# Настройка на работната директория
WORKDIR /app

# Копиране на requirements
COPY requirements.txt .

# Инсталиране на зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копиране на останалите файлове
COPY . .

# Експониране на порта
EXPOSE 5000

# Стартиране на приложението
CMD ["python", "app.py"]

