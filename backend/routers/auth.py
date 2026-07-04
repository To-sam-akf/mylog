from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session, SQLModel
from backend.database import get_session
from backend.security import create_access_token,verify_password, get_current_user
from backend.models.user import User

router=APIRouter(prefix="/api/auth",tags=["auth"])

class LoginRequest(SQLModel):
    username:str
    password:str

@router.post("/login")
def login(data:LoginRequest,session:Session=Depends(get_session))->dict: 
    user=session.exec(select(User).where(User.username==data.username)).first()

    if not user or not verify_password(data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    
    token=create_access_token({
        "sub":str(user.id),
        "username":user.username,
        "role":user.role,
    })
    return {
        "access_token":token,
        "token_type":"bearer",
    }

@router.get("/me")
def get_me(current_user:User=Depends(get_current_user)):
    return {
        "username":current_user.username,
        "role": current_user.role
    }
