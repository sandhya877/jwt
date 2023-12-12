from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

import urllib.parse

# PostgreSQL database configuration
password = "Postgresql@678"
encoded_password = urllib.parse.quote_plus(password)

DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/DATA1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI application
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI route to create a new user
@app.post("/users/")
def create_user(username: str, email: str, full_name: str, db: Session = Depends(get_db)):
    new_user = User(username=username, email=email, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
