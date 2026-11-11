
from app.database import Base, engine
from app.models import User


def init_db():
    """Create database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables initialized successfully.")

