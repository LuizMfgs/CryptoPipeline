from app.database.Database import engine
from app.database.Models import Base


def init_database():
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_database()
    