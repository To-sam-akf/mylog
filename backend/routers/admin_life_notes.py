from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select

from backend.database import get_session
from backend.models.life_note import LifeNote
from backend.models.user import User
from backend.security import require_admin

router = APIRouter(prefix="/api/admin/life-notes", tags=["admin-life-notes"])


class LifeNoteUpdateRequest(SQLModel):
    title: str
    content: str
    content_markdown: Optional[str] = None


@router.put("")
def update_life_notes(
    data: LifeNoteUpdateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
) -> dict:
    note = session.exec(select(LifeNote).order_by(LifeNote.id)).first()

    if not note:
        raise HTTPException(status_code=404, detail="Life Notes not found")

    title = data.title.strip()
    content = data.content.strip()

    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be empty")

    if not content:
        raise HTTPException(status_code=422, detail="Content cannot be empty")

    note.title = title
    note.content = data.content
    note.content_markdown = data.content_markdown
    note.updated_at = datetime.now()

    session.commit()
    session.refresh(note)

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "content_markdown": note.content_markdown,
        "updated_at": note.updated_at,
    }
