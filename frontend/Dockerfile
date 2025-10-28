# Frontend Dockerfile - Astro
FROM node:20-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy project files
COPY . .

# Expose port
EXPOSE 4321

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
