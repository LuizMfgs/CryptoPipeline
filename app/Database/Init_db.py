from app.Database.Database import engine
from app.Database.Models import Base


def init_database():

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")