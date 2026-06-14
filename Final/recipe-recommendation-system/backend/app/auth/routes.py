# backend/app/auth/routes.py
# Updated to handle all personalization fields

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token, UserProfile
from .password_utils import hash_password, verify_password
from .jwt_handler import create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/signup", response_model=UserProfile)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Enhanced signup with full personalization:
    - Dietary preferences
    - Health conditions
    - Allergies
    - Preferred cuisines
    """
    # Check if user exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with all personalization fields
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        age=user.age,
        dietary_type=user.dietary_type,
        health_conditions=user.health_conditions if user.health_conditions else [],
        allergies=user.allergies if user.allergies else [],  # NEW
        preferred_cuisines=user.preferred_cuisines if user.preferred_cuisines else []  # NEW
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ New user created with preferences:")
    print(f"   - Dietary: {new_user.dietary_type}")
    print(f"   - Allergies: {new_user.allergies}")
    print(f"   - Preferred Cuisines: {new_user.preferred_cuisines}")
    print(f"   - Health Conditions: {new_user.health_conditions}")
    
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfile)
def get_current_user_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user profile with all preferences"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency to get current user"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user