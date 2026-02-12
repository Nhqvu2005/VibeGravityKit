#!/usr/bin/env python3
"""
Docker Wizard — Generate Dockerfile & Compose.

Usage:
    python docker_gen.py --stack node
    python docker_gen.py --stack python --db result
"""

import argparse

TEMPLATES = {
    "node": {
        "dockerfile": """FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["npm", "start"]""",
        "compose": """version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production"""
    },
    "python": {
        "dockerfile": """FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]""",
        "compose": """version: '3.8'
services:
  app:
    build: .
    environment:
      - PYTHONUNBUFFERED=1"""
    }
}

DB_TEMPLATES = {
    "postgres": """
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data""",
    "redis": """
  redis:
    image: redis:alpine"""
}

def generate(stack, db):
    print("🐳 Generating Docker config...")
    
    tmpl = TEMPLATES.get(stack, TEMPLATES["node"])
    
    print("\n📄 Dockerfile:")
    print(tmpl["dockerfile"])
    
    compose = tmpl["compose"]
    if db:
        compose += DB_TEMPLATES.get(db, "")
        if db == "postgres":
            compose += "\nvolumes:\n  db_data:"
            
    print("\n🐙 docker-compose.yml:")
    print(compose)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack", choices=["node", "python"], required=True)
    parser.add_argument("--db", choices=["postgres", "redis"])
    args = parser.parse_args()
    generate(args.stack, args.db)

if __name__ == "__main__":
    main()
