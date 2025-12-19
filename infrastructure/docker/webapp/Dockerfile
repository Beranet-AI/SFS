# =========================
# Stage 1 — Build Next.js
# =========================
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (better cache)
COPY package.json package-lock.json ./
RUN npm install --no-audit --no-fund


# Copy the rest of the source code (including src/, public/, next.config.js, etc.)
COPY . .

# Build Next.js (production build)
RUN npm run build


# =========================
# Stage 2 — Nginx Runtime
# =========================
FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config (from webapp source tree)
COPY src/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy Next.js build artifacts for static serving
COPY --from=builder /app/.next /usr/share/nginx/html/.next

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
