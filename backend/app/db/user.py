from sqlalchemy.orm import Session
from app.models.user import User, UserRole

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    user = User(**user_data, role=UserRole.USER.value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user