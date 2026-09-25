import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


async def get_connection():
    connection = await asyncpg.connect(
        user="postgres",
        password=os.getenv("PASSWORD_DB"),
        database="menu_db",
        host="localhost",
        port=5432
    )
    return connection

async def create_tables():
    connection = await get_connection()
    try:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            )
        """)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS dishes(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                category_id INTEGER REFERENCES categories(id)
                ON DELETE SET NULL
            )
        """)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                dish_id INTEGER REFERENCES dishes(id)
                ON DELETE SET NULL,
                quantity INTEGER NOT NULL,
                total_price NUMERIC(10, 2) NOT NULL,
                user_id INTEGER REFERENCES users(id)
                ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Таблицы созданы")

    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()