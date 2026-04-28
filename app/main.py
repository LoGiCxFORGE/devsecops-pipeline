from fastapi import FastAPI
from app.db import get_db_connection

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello DevSecOps"}


# 🚨 SQL Injection Vulnerability
@app.get("/users/{username}")
def get_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # ❌ Vulnerable way (f-string SQL)
    query = f"SELECT * FROM users WHERE username = '{username}'"  # nosec B608
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    return {"user": user}
