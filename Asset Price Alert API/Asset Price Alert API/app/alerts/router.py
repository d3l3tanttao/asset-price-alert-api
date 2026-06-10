from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.assets.schemas import AlertResponse
from app.assets.service import get_alert_by_id, list_alerts
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.users.models import User


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AlertResponse]:
    return list_alerts(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AlertResponse:
    alert = get_alert_by_id(
        db=db,
        user_id=current_user.id,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert