from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TrackedAssetCreateRequest(BaseModel):
    symbol: str = Field(min_length=2, max_length=20)
    name: str | None = Field(default=None, max_length=255)
    target_price: Decimal = Field(gt=0)
    condition: Literal["below", "above"] = "below"
    currency: str = Field(default="USD", min_length=3, max_length=10)


class TrackedAssetResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    name: str | None
    target_price: Decimal
    condition: str
    currency: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class PriceCheckResponse(BaseModel):
    id: int
    tracked_asset_id: int
    price: Decimal
    currency: str
    source: str
    checked_at: datetime

    model_config = {
        "from_attributes": True,
    }
class AlertResponse(BaseModel):
    id: int
    user_id: int
    tracked_asset_id: int
    price_check_id: int
    message: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class ManualPriceCheckResponse(BaseModel):
    tracked_asset: TrackedAssetResponse
    price_check: PriceCheckResponse
    alert_triggered: bool
    alert: AlertResponse | None

class EnqueuePriceCheckResponse(BaseModel):
    job_id: str
    status: str
    asset_id: int