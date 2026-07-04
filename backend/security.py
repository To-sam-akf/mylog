from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlmodel import Session, select

from backend.database import get_session
from backend.models.user import User

load_dotenv()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "dev-secret")
JWT_ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(getenv("JWT_EXPIRE_MINUTES", "1440"))

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password,password_hash)

def create_access_token(data:dict) ->str:
    payload=data.copy()
    # 计算过期时间
    expire=datetime.utcnow()+timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload.update({"exp":expire})
    # 签名并编码
    return jwt.encode(payload,JWT_SECRET_KEY,JWT_ALGORITHM)

bearer_scheme=HTTPBearer(auto_error=False)



def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(token=token,key=JWT_SECRET_KEY,algorithms=JWT_ALGORITHM)
    except JWTError as exc:
        raise HTTPException(status_code=401,detail="invalid or expired token") from exc

def get_current_user(
        credentials:HTTPAuthorizationCredentials | None=Depends(bearer_scheme),
        session: Session=Depends(get_session)
)->User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload=decode_access_token(credentials.credentials)
    user_id=payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401,detail="Invalid token")
    user=session.exec(select(User).where(int(user_id)==User.id)).first()
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return user

# 管理员校验
def require_admin(current_user:User=Depends(get_current_user))->User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin permission required")
    return current_user
