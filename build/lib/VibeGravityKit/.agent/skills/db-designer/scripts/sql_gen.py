#!/usr/bin/env python3
"""
Database Designer — Generate SQL / Prisma Schemas.

Usage:
    python sql_gen.py --models "User, Product" --format prisma
"""

import argparse

TEMPLATES = {
    "User": {
        "sql": """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",
        "prisma": """model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  password  String
  fullName  String?
  role      String   @default("user")
  createdAt DateTime @default(now())
  posts     Post[]
  orders    Order[]
}"""
    },
    "Product": {
        "sql": """CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",
        "prisma": """model Product {
  id          Int      @id @default(autoincrement())
  name        String
  slug        String   @unique
  price       Decimal
  stock       Int      @default(0)
  description String?
  createdAt   DateTime @default(now())
  orderItems  OrderItem[]
}"""
    }
}

def generate_schema(models, fmt):
    model_list = [m.strip() for m in models.split(",")]
    
    print("\n" + "="*50)
    print(f"🗄️  GENERATED {fmt.upper()} SCHEMA")
    print("="*50 + "\n")
    
    for m in model_list:
        # Match case insensitive
        found = False
        for k, v in TEMPLATES.items():
            if k.lower() == m.lower():
                print(v.get(fmt, f"-- No template for {m} in {fmt}"))
                print("")
                found = True
                break
        
        if not found:
            # Generic fallback
            if fmt == "sql":
                print(f"CREATE TABLE {m.lower()}s (id SERIAL PRIMARY KEY, name VARCHAR(255));")
            elif fmt == "prisma":
                print(f"model {m} {{\n  id Int @id @default(autoincrement())\n}}")
                
    print("\n" + "="*50)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, required=True)
    parser.add_argument("--format", type=str, choices=["sql", "prisma"], default="sql")
    
    args = parser.parse_args()
    generate_schema(args.models, args.format)

if __name__ == "__main__":
    main()
