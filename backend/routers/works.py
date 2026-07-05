from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.database import get_session
from backend.models.work import Work, WorkPageSetting

router = APIRouter(prefix="/api/works", tags=["works"])


def serialize_work(work: Work) -> dict:
    return {
        "id": work.id,
        "name": work.name,
        "tech": work.tech,
        "desc": work.desc,
        "status": work.status,
        "github": work.github,
        "color": work.color,
        "sort_order": work.sort_order,
        "updated_at": work.updated_at,
    }


@router.get("")
def get_works(session: Session = Depends(get_session)) -> dict:
    setting = session.exec(select(WorkPageSetting).order_by(WorkPageSetting.id)).first()  # type: ignore[arg-type]

    if not setting:
        raise HTTPException(status_code=404, detail="Works settings not found")

    works = session.exec(select(Work).order_by(Work.sort_order, Work.id)).all()  # type: ignore[arg-type]

    return {
        "title": setting.title,
        "subtitle": setting.subtitle,
        "description": setting.description,
        "projects": [serialize_work(work) for work in works],
    }
