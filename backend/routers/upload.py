from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pathlib import Path
from uuid import uuid4
from backend.models.user import User
from backend.models.asset import Asset
from backend.security import require_admin
from sqlmodel import Session,select
from backend.database import get_session


router = APIRouter(prefix="/api/admin/upload", tags=["admin-upload"])

UPLOAD_DIR = Path("static/uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

ALLOWED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

@router.post("/image")
async def upload_image(
    file:UploadFile=File(...),
    current_user:User=Depends(require_admin),
    session:Session=Depends(get_session)
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds limit")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    suffix=ALLOWED_MIME_TYPES[file.content_type]
    # 生成一个唯一的文件名：
    filename=f"{uuid4().hex}{suffix}"
    file_path=UPLOAD_DIR/filename
    # 写回文件到file_path
    file_path.write_bytes(content)

    # 数据库中记录 `url`
    url=f"/static/uploads/{filename}"
    asset=Asset(
        filename=filename,
        url=url,
        uploaded_by=current_user.id,
        mime_type=file.content_type,
        file_size=len(content),
        original_filename=file.filename or filename
    )

    session.add(asset)
    session.commit()
    session.refresh(asset)

    return {
         "id": asset.id,
        "url": asset.url,
        "filename": asset.filename,
        "original_name": asset.original_filename,
        "mime_type": asset.mime_type,
        "file_size": asset.file_size,
    }