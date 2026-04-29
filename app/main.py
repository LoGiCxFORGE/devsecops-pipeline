from fastapi import FastAPI
from app.db import get_db_connection


app = FastAPI()


@app.middleware("http")
async def security_headers_middleware(request, call_next):
    response = await call_next(request)

    # Standard headers for "Non-Storable Content" [10049]
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # Anti-sniffing and CORP
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

    return response


# Also, add these to stop ZAP from complaining about missing files
@app.get("/robots.txt", include_in_schema=False)
@app.get("/sitemap.xml", include_in_schema=False)
async def disable_crawlers():
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse("User-agent: *\nDisallow: /")


@app.get("/")
def read_root():
    return {"message": "Hello DevSecOps"}


# 🚨 SQL Injection Vulnerability
@app.get("/users/{username}")
def get_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # ❌ Vulnerable way (f-string SQL)
    # query = f"SELECT * FROM users WHERE username = '{username}'"  # nosec B608
    # cursor.execute(query)

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))  # The database driver handles the safety

    user = cursor.fetchone()
    conn.close()

    return {"user": user}
