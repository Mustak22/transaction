from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi import HTTPException, status
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
router = APIRouter()

security = HTTPBasic()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin123"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.post("/items/")
def create_item(item: List[schemas.ItemCreate], db: Session = Depends(get_db), username: str = Depends(verify_user)):
    db_items = [models.Item(**item.dict()) for item in item]
    db.add_all(db_items)
    db.commit()
    return {"message": f"{len(db_items)} records inserted"}

