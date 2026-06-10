from app.assets.models import Alert, PriceCheck, TrackedAsset
from app.assets.service import create_price_check, get_tracked_asset_by_id
from app.database import SessionLocal
from app.users.models import User


def run_price_check_job(
    user_id: int,
    asset_id: int,
    ) -> dict[str, object]:
    db = SessionLocal()

    try:
        tracked_asset = get_tracked_asset_by_id(
            db=db,
            user_id=user_id,
            asset_id=asset_id,
            )

        if tracked_asset is None:
            return {
                "status": "not_found",
                "asset_id": asset_id,
                }

        price_check, alert_triggered, alert = create_price_check(
            db=db,
            tracked_asset=tracked_asset,
            )

        return {
            "status": "completed",
            "asset_id": asset_id,
            "price_check_id": price_check.id,
            "alert_triggered": alert_triggered,
            "alert_id": alert.id if alert is not None else None,
        }
    finally:
        db.close()