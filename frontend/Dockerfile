FROM node:20-alpine

WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Запуск dev сервера (для разработки)
# В продакшене используйте адаптер static и nginx
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

