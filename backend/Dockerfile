FROM python:3.11-slim

WORKDIR /app

ARG NODE_ENV=development
ENV NODE_ENV=$NODE_ENV

RUN apt-get update && apt-get install -y \
   build-essential \
   && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

CMD if [ "$NODE_ENV" = "production" ]; then \
       uvicorn main:app --host 0.0.0.0 --port 8000; \
   else \
       uvicorn main:app --host 0.0.0.0 --port 8000 --reload; \
   fi