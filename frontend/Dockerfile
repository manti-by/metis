FROM node:22-alpine

WORKDIR /app

COPY frontend/package.json frontend/tsconfig*.json ./
COPY frontend/package-lock.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

EXPOSE 3003

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3003"]
