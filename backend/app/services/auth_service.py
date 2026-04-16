from sqlalchemy.orm import Session

from app.repositories.user_repository import create_user, get_user_by_email
from app.utils.security import create_access_token, hash_password, verify_password


def register_user(db: Session, name: str, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(password)
    user = create_user(db, name=name, email=email, password_hash=hashed_password)
    return user


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": user}