# # # backend/Dockerfile

# # # 1. Използваме официален Python образ
# # FROM python:3.11-slim

# # # 2. Създаваме директория в контейнера за приложението
# # WORKDIR /app

# # # 3. Копираме зависимостите (ако имаш requirements.txt)
# # COPY requirements.txt .

# # # 4. Инсталираме зависимостите
# # RUN pip install --no-cache-dir -r requirements.txt

# # # 5. Копираме целия backend код
# # COPY . .

# # # 6. Излагаме порт (по избор)
# # EXPOSE 5000

# # # 7. Задаваме командата за стартиране на Flask
# # CMD ["python", "app.py"]



# # Билдна част за React
# # FROM node:20 AS frontend-build
# # WORKDIR /app/frontend
# # COPY frontend/ ./
# # RUN npm install
# # RUN npm run build

# # # Flask бекенд + React static
# # FROM python:3.11-slim AS backend
# # WORKDIR /app

# # # Инсталиране на Python зависимости
# # COPY requirements.txt .
# # RUN pip install --no-cache-dir -r requirements.txt

# # # Копиране на бекенда
# # COPY app/ ./app/

# # # Копиране на React билд файловете в бекенда
# # COPY --from=frontend-build /app/frontend/dist ./frontend_dist

# # # Flask ще чете от тази папка
# # ENV FLASK_APP=app/app.py
# # ENV FLASK_RUN_HOST=0.0.0.0
# # ENV FLASK_ENV=production

# # CMD ["flask", "run"]

# FROM node:20 AS frontend-build
# WORKDIR /app/frontend 
# #Може да променя двете точки
# COPY frontend/ ./
# RUN npm install
# RUN npm run build

# # === Stage 2: Flask API + Static Files ===
# FROM python:3.11-slim AS backend
# WORKDIR /app

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy Flask app
# COPY . .

# # Copy built React files
# COPY --from=frontend-build /app/frontend/dist ./frontend_dist

# # Env variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_ENV=production

# # Start Flask
# CMD ["flask", "run"]


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

