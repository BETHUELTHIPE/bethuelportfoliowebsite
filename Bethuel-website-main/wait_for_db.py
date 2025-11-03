import time
import psycopg2
import os

db_host = os.environ.get("POSTGRES_HOST", "db")
db_name = os.environ.get("POSTGRES_DB", "Bethuelresumedb")
db_user = os.environ.get("POSTGRES_USER", "Bethuel")
db_pass = os.environ.get("POSTGRES_PASSWORD", "23498812")
db_port = os.environ.get("POSTGRES_PORT", "5432")

while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            port=db_port
        )
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(2)
