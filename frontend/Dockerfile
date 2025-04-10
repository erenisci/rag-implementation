FROM node:22.14.0-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY public/ ./public/
COPY src/ ./src/
COPY index.html ./
COPY vite.config.ts ./
COPY tsconfig.json ./
COPY tsconfig.app.json ./
COPY tsconfig.node.json ./
COPY eslint.config.js ./

RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "preview", "--", "--port", "3000", "--host"]
