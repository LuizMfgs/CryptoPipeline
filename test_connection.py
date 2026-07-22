from sqlalchemy import text

from app.Database.Database import engine

with engine.connect() as conn:
    print(conn.execute(text("SELECT version();")).scalar())