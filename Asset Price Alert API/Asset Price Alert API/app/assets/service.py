from decimal import Decimal

from sqlalchemy.orm import Session

from app.assets.models import Alert, PriceCheck, TrackedAsset
from app.pricing.provider import get_current_price


def create_tracked_asset(
    db: Session,
    user_id: int,
    symbol: str,
    target_price: Decimal,
    condition: str,
    currency: str,
    name: str | None = None,
) -> TrackedAsset:
    tracked_asset = TrackedAsset(
        user_id=user_id,
        symbol=symbol.upper(),
        name=name,
        target_price=target_price,
        condition=condition,
        currency=currency.upper(),
    )

    db.add(tracked_asset)
    db.commit()
    db.refresh(tracked_asset)

    return tracked_asset


def list_tracked_assets(
    db: Session,
    user_id: int,
) -> list[TrackedAsset]:
    return (
        db.query(TrackedAsset)
        .filter(TrackedAsset.user_id == user_id)
        .order_by(TrackedAsset.created_at.desc())
        .all()
    )


def get_tracked_asset_by_id(
    db: Session,
    user_id: int,
    asset_id: int,
) -> TrackedAsset | None:
    return (
        db.query(TrackedAsset)
        .filter(
            TrackedAsset.id == asset_id,
            TrackedAsset.user_id == user_id,
        )
        .first()
    )


def delete_tracked_asset(
    db: Session,
    tracked_asset: TrackedAsset,
) -> None:
    db.delete(tracked_asset)
    db.commit()


def create_price_check(
    db: Session,
    tracked_asset: TrackedAsset,
) -> tuple[PriceCheck, bool, Alert | None]:
    current_price = get_current_price(tracked_asset.symbol)

    price_check = PriceCheck(
        tracked_asset_id=tracked_asset.id,
        price=current_price,
        currency=tracked_asset.currency,
        source="mock",
    )

    alert_triggered = is_alert_triggered(
        current_price=current_price,
        target_price=tracked_asset.target_price,
        condition=tracked_asset.condition,
    )

    db.add(price_check)
    db.commit()
    db.refresh(price_check)

    alert = None

    if alert_triggered:
        alert = create_alert(
            db=db,
            tracked_asset=tracked_asset,
            price_check=price_check,
        )

    return price_check, alert_triggered, alert


def list_price_checks(
    db: Session,
    tracked_asset: TrackedAsset,
) -> list[PriceCheck]:
    return (
        db.query(PriceCheck)
        .filter(PriceCheck.tracked_asset_id == tracked_asset.id)
        .order_by(PriceCheck.checked_at.desc())
        .all()
    )


def is_alert_triggered(
    current_price: Decimal,
    target_price: Decimal,
    condition: str,
) -> bool:
    if condition == "below":
        return current_price <= target_price

    if condition == "above":
        return current_price >= target_price

    return False

def create_alert(
    db: Session,
    tracked_asset: TrackedAsset,
    price_check: PriceCheck,
) -> Alert:
    message = (
        f"{tracked_asset.symbol} reached alert condition: "
        f"current price {price_check.price} {price_check.currency}, "
        f"target {tracked_asset.target_price} {tracked_asset.currency}, "
        f"condition {tracked_asset.condition}."
    )

    alert = Alert(
        user_id=tracked_asset.user_id,
        tracked_asset_id=tracked_asset.id,
        price_check_id=price_check.id,
        message=message,
        status="created",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert

def list_alerts(
    db: Session,
    user_id: int,
) -> list[Alert]:
    return (
        db.query(Alert)
        .filter(Alert.user_id == user_id)
        .order_by(Alert.created_at.desc())
        .all()
    )


def get_alert_by_id(
    db: Session,
    user_id: int,
    alert_id: int,
) -> Alert | None:
    return (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == user_id,
        )
        .first()
    )