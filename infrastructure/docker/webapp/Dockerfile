# =========================
# Build stage
# =========================
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies (cache-friendly)
COPY frontend/webapp/package*.json ./
RUN npm install --no-audit --no-fund

# Copy source and build
COPY frontend/webapp .
RUN npm run build

# =========================
# Runtime stage
# =========================
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app ./

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]
