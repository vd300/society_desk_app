import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import Resident, User
from app.models.enums import UserRole
from app.repositories.user_repository import get_user_by_id

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    user_id = payload.get("sub")
    user = get_user_by_id(db, str(user_id)) if user_id else None
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(*roles: UserRole):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return dependency


def require_admin(current_user: User = Depends(require_role(UserRole.ADMIN))) -> User:
    return current_user


def require_resident(current_user: User = Depends(require_role(UserRole.RESIDENT))) -> User:
    return current_user


def require_security(current_user: User = Depends(require_role(UserRole.SECURITY))) -> User:
    return current_user


def require_notice_viewer(
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.RESIDENT, UserRole.SECURITY)),
) -> User:
    return current_user


def get_current_resident(
    current_user: User = Depends(require_resident),
    db: Session = Depends(get_db),
) -> Resident:
    if not current_user.resident_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resident profile not found")
    return current_user.resident_profile
