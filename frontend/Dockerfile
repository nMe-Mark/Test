FROM node:18

WORKDIR /app

# Копирай package файловете
COPY package*.json ./

# Инсталирай всички зависимости (включително axios, ако е добавен в package.json)
RUN npm install

# Копирай останалите файлове
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
