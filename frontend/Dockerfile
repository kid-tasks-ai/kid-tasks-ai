FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json  ./
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Start the application
CMD ["npm", "run", "dev"]