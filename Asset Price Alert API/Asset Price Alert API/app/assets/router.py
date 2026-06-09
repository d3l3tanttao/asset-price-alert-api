from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.assets.schemas import (
    ManualPriceCheckResponse,
    PriceCheckResponse,
    TrackedAssetCreateRequest,
    TrackedAssetResponse,
)
from app.assets.service import (
    create_price_check,
    create_tracked_asset,
    delete_tracked_asset,
    get_tracked_asset_by_id,
    list_price_checks,
    list_tracked_assets,
)
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.users.models import User


router = APIRouter(
    prefix="/tracked-assets",
    tags=["Tracked Assets"],
)


@router.post(
    "",
    response_model=TrackedAssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset(
    payload: TrackedAssetCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TrackedAssetResponse:
    return create_tracked_asset(
        db=db,
        user_id=current_user.id,
        symbol=payload.symbol,
        name=payload.name,
        target_price=payload.target_price,
        condition=payload.condition,
        currency=payload.currency,
    )


@router.get(
    "",
    response_model=list[TrackedAssetResponse],
)
def get_assets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[TrackedAssetResponse]:
    return list_tracked_assets(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{asset_id}",
    response_model=TrackedAssetResponse,
)
def get_asset(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TrackedAssetResponse:
    tracked_asset = get_tracked_asset_by_id(
        db=db,
        user_id=current_user.id,
        asset_id=asset_id,
    )

    if tracked_asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracked asset not found.",
        )

    return tracked_asset


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_asset(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    tracked_asset = get_tracked_asset_by_id(
        db=db,
        user_id=current_user.id,
        asset_id=asset_id,
    )

    if tracked_asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracked asset not found.",
        )

    delete_tracked_asset(
        db=db,
        tracked_asset=tracked_asset,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{asset_id}/check-now",
    response_model=ManualPriceCheckResponse,
)
def check_asset_now(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ManualPriceCheckResponse:
    tracked_asset = get_tracked_asset_by_id(
        db=db,
        user_id=current_user.id,
        asset_id=asset_id,
    )

    if tracked_asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracked asset not found.",
        )

    price_check, alert_triggered = create_price_check(
        db=db,
        tracked_asset=tracked_asset,
    )

    return ManualPriceCheckResponse(
        tracked_asset=tracked_asset,
        price_check=price_check,
        alert_triggered=alert_triggered,
    )


@router.get(
    "/{asset_id}/price-history",
    response_model=list[PriceCheckResponse],
)
def get_price_history(
    asset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PriceCheckResponse]:
    tracked_asset = get_tracked_asset_by_id(
        db=db,
        user_id=current_user.id,
        asset_id=asset_id,
    )

    if tracked_asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tracked asset not found.",
        )

    return list_price_checks(
        db=db,
        tracked_asset=tracked_asset,
    )