FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

ENV HOST=0.0.0.0
ENV PORT=3000

# Start the application
CMD ["npm", "run", "dev"]
