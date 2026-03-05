FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
EXPOSE 5173
CMD ["node_modules/.bin/vite", "--host", "0.0.0.0"]
