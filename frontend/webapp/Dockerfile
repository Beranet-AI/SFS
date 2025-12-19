# =========================
# 1️⃣ Build stage
# =========================
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# =========================
# 2️⃣ Runtime stage (Nginx)
# =========================
FROM nginx:1.27-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy Next.js build output
COPY --from=builder /app/.next /usr/share/nginx/html/.next
COPY --from=builder /app/public /usr/share/nginx/html/public
COPY --from=builder /app/package.json /usr/share/nginx/html/package.json

# Next.js standalone (اگر بعداً فعالش کنی)
# COPY --from=builder /app/.next/standalone /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
