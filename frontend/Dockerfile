FROM node:20-slim

WORKDIR /app

ARG NODE_ENV=development
ENV NODE_ENV=$NODE_ENV

COPY package*.json ./
RUN npm install

COPY . .

ENV HOST=0.0.0.0
ENV PORT=3000

CMD if [ "$NODE_ENV" = "production" ]; then \
       npm run build && npm run start; \
   else \
       npm run dev; \
   fi