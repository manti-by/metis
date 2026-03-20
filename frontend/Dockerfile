FROM node:22-alpine

WORKDIR /app

COPY frontend/package.json frontend/tsconfig*.json ./
RUN npm install

EXPOSE 3003

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
