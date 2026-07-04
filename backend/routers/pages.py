from sqlmodel import Session,select
from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_session
from ..models.page import Page

router = APIRouter(prefix="/api/pages", tags=["pages"])

@router.get("/{slug}")
def get_pages(slug: str, session: Session = Depends(get_session)):
    page=session.exec(select(Page).where(Page.slug==slug)).first()

    if not page:
        raise HTTPException(status_code=404,detail="Page not found")
    
    return {
        "slug":page.slug,
        "title":page.title,
        "content":page.content,
        "updated_at":page.updated_at,
    }