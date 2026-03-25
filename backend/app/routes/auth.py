from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/seed-admin")
def seed_admin(db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == "admin@example.com").first()
    if existing:
        return {"message": "Admin already exists", "email": existing.email, "password": "admin123"}
    user = User(
        full_name="System Administrator",
        email="admin@example.com",
        password_hash=hash_password("admin123"),
        role="super_admin",
    )
    db.add(user)
    db.commit()
    return {"message": "Admin created", "email": user.email, "password": "admin123"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
    }
