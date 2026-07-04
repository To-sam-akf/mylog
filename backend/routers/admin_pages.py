from fastapi import APIRouter,Depends, HTTPException
from typing import Optional
from sqlmodel import select, Session, SQLModel
from backend.database import get_session
from backend.models.page import Page
from datetime import datetime
from backend.models.page_version import PageVersion
from backend.models.user import User
from backend.security import require_admin

router=APIRouter(prefix="/api/admin/{pages}",tags=["admin-pages"])

class PageUpdateRequest(SQLModel):
    title:str
    content:str
    content_markdown:Optional[str]=None
@router.put("/{slug}")
def update_page(
    slug:str,
    data:Page,
    session:Session=Depends(get_session),
    current_user:User=Depends(require_admin)
)->dict:
    page=session.exec(select(Page).where(slug==Page.slug)).first()
    if not page:
        raise HTTPException(status_code=404,detail="not found page")
    title=data.title.strip()
    content=data.content.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be empty")

    if not content:
        raise HTTPException(status_code=422, detail="Content cannot be empty")
    
    # 记录历史版本
    assert page.id is not None  # 从数据库查出来的 page 一定有 id
    page_version=PageVersion(
        page_id=page.id,
        title=page.title,
        content=page.content,
        content_markdown=page.content_markdown,
        created_by=current_user.id
    )
    session.add(page_version)

    page.title=title
    page.content=data.content
    page.content_markdown=data.content_markdown
    page.updated_at=datetime.now()

    session.commit()
    session.refresh(page)
    
    return {
         "slug": page.slug,
        "title": page.title,
        "content": page.content,
        "content_markdown": page.content_markdown,
        "updated_at": page.updated_at,
    }
