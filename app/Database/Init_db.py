from app.Database.Database import engine
from app.Database.Models import Base


def init_database():
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_database()
    