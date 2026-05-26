from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


def save_upload(upload: UploadFile, folder: str) -> str:
    settings = get_settings()
    upload_root = Path(settings.upload_dir)
    target_dir = upload_root / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename or "").suffix
    filename = f"{uuid4()}{suffix}"
    target = target_dir / filename
    with target.open("wb") as file:
        file.write(upload.file.read())
    return str(target).replace("\\", "/")
