from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select

from backend.database import get_session
from backend.models.user import User
from backend.models.work import Work, WorkPageSetting
from backend.routers.works import serialize_work
from backend.security import require_admin

router = APIRouter(prefix="/api/admin/works", tags=["admin-works"])


class WorkSettingsUpdateRequest(SQLModel):
    title: str
    subtitle: str
    description: str


class WorkRequest(SQLModel):
    name: str
    tech: str
    desc: str
    status: str
    github: str
    color: str = "yellow"
    sort_order: int = 0


def validate_work_data(data: WorkRequest) -> dict:
    work_data = {
        "name": data.name.strip(),
        "tech": data.tech.strip(),
        "desc": data.desc.strip(),
        "status": data.status.strip(),
        "github": data.github.strip(),
        "color": data.color.strip() or "yellow",
        "sort_order": data.sort_order,
    }

    if not work_data["name"]:
        raise HTTPException(status_code=422, detail="Work name cannot be empty")

    if not work_data["github"]:
        raise HTTPException(status_code=422, detail="Work github cannot be empty")

    return work_data


@router.put("/settings")
def update_work_settings(
    data: WorkSettingsUpdateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
) -> dict:
    setting = session.exec(select(WorkPageSetting).order_by(WorkPageSetting.id)).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Works settings not found")

    title = data.title.strip()
    subtitle = data.subtitle.strip()
    description = data.description.strip()

    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be empty")

    if not subtitle:
        raise HTTPException(status_code=422, detail="Subtitle cannot be empty")

    if not description:
        raise HTTPException(status_code=422, detail="Description cannot be empty")

    setting.title = title
    setting.subtitle = subtitle
    setting.description = description
    setting.updated_at = datetime.now()

    session.commit()
    session.refresh(setting)

    return {
        "title": setting.title,
        "subtitle": setting.subtitle,
        "description": setting.description,
        "updated_at": setting.updated_at,
    }


@router.post("")
def create_work(
    data: WorkRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
) -> dict:
    work = Work(**validate_work_data(data))
    session.add(work)
    session.commit()
    session.refresh(work)

    return serialize_work(work)


@router.put("/{work_id}")
def update_work(
    work_id: int,
    data: WorkRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
) -> dict:
    work = session.get(Work, work_id)

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    work_data = validate_work_data(data)
    work.name = work_data["name"]
    work.tech = work_data["tech"]
    work.desc = work_data["desc"]
    work.status = work_data["status"]
    work.github = work_data["github"]
    work.color = work_data["color"]
    work.sort_order = work_data["sort_order"]
    work.updated_at = datetime.now()

    session.commit()
    session.refresh(work)

    return serialize_work(work)


@router.delete("/{work_id}")
def delete_work(
    work_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
) -> dict:
    work = session.get(Work, work_id)

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    session.delete(work)
    session.commit()

    return {"ok": True}
