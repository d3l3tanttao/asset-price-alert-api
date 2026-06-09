from decimal import Decimal


MOCK_PRICES: dict[str, Decimal] = {
    "BTC": Decimal("68000.00"),
    "ETH": Decimal("3500.00"),
    "SOL": Decimal("150.00"),
    "AAPL": Decimal("195.00"),
    "TSLA": Decimal("250.00"),
}


def get_current_price(symbol: str) -> Decimal:
    normalized_symbol = symbol.upper()

    return MOCK_PRICES.get(
        normalized_symbol,
        Decimal("100.00"),
    )