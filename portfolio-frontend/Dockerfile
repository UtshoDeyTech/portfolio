# Multi-stage build for Astro application
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application (creates static files in dist/)
RUN npm run build

# Stage 2: Production with lightweight server
FROM node:20-alpine

WORKDIR /app

# Install a simple HTTP server for serving static files
RUN npm install -g sirv-cli

# Copy built static files from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 4321

# Serve static files with sirv (production-ready server)
# --host 0.0.0.0 allows external connections
# --port 4321 matches our exposed port
# --single makes it work with client-side routing
CMD ["sirv", "dist", "--host", "0.0.0.0", "--port", "4321", "--single"]
