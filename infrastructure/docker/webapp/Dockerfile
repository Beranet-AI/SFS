FROM node:20-alpine

WORKDIR /app

COPY frontend/webapp/package*.json ./
RUN npm ci

COPY frontend/webapp ./

# Build
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]
