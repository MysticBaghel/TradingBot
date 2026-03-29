VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s.isalpha() or len(s) < 3:
        raise ValidationError(f"Invalid symbol: '{symbol}'. Example: BTCUSDT")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Side must be BUY or SELL, got: '{side}'")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be MARKET or LIMIT, got: '{order_type}'")
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
        if q <= 0:
            raise ValidationError("Quantity must be greater than 0")
        return q
    except ValueError:
        raise ValidationError(f"Invalid quantity: '{quantity}'. Must be a number.")


def validate_price(price: str) -> float:
    try:
        p = float(price)
        if p <= 0:
            raise ValidationError("Price must be greater than 0")
        return p
    except ValueError:
        raise ValidationError(f"Invalid price: '{price}'. Must be a number.")
