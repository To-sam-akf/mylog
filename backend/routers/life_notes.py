from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.database import get_session
from backend.models.life_note import LifeNote

router = APIRouter(prefix="/api/life-notes", tags=["life-notes"])


@router.get("")
def get_life_notes(session: Session = Depends(get_session)) -> dict:
    note = session.exec(select(LifeNote).order_by(LifeNote.id)).first()

    if not note:
        raise HTTPException(status_code=404, detail="Life Notes not found")

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "content_markdown": note.content_markdown,
        "updated_at": note.updated_at,
    }
