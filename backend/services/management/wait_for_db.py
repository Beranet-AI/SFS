import os
import time
import psycopg2


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST", "db"),
                port=os.getenv("POSTGRES_PORT", "5432"),
            )
            conn.close()
            print("Database is ready ✅")
            break
        except Exception as exc:
            print(f"Waiting for database: {exc}", flush=True)
            time.sleep(2)


if __name__ == "__main__":
    wait_for_db()
