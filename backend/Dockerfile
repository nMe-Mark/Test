# backend/Dockerfile

# 1. Използваме официален Python образ
FROM python:3.11-slim

# 2. Създаваме директория в контейнера за приложението
WORKDIR /app

# 3. Копираме зависимостите (ако имаш requirements.txt)
COPY requirements.txt .

# 4. Инсталираме зависимостите
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копираме целия backend код
COPY . .

# 6. Излагаме порт (по избор)
EXPOSE 5000

# 7. Задаваме командата за стартиране на Flask
CMD ["python", "app.py"]
