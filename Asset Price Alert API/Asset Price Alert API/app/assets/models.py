from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TrackedAsset(Base):
    __tablename__ = "tracked_assets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        index=True,
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    target_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
    )

    condition: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="below",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="USD",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    price_checks: Mapped[list["PriceCheck"]] = relationship(
        back_populates="tracked_asset",
        cascade="all, delete-orphan",
    )


class PriceCheck(Base):
    __tablename__ = "price_checks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    tracked_asset_id: Mapped[int] = mapped_column(
        ForeignKey("tracked_assets.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="USD",
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="mock",
    )

    checked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    tracked_asset: Mapped[TrackedAsset] = relationship(
        back_populates="price_checks",
    )