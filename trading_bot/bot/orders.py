import logging
from bot.client import BinanceClient
from bot.validators import (
    validate_symbol, validate_side,
    validate_order_type, validate_quantity, validate_price,
    ValidationError,
)

logger = logging.getLogger(__name__)


def print_order_summary(order_type: str, symbol: str, side: str, quantity: float, price: float = None):
    print("\n" + "=" * 45)
    print("        ORDER REQUEST SUMMARY")
    print("=" * 45)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("=" * 45)


def print_order_response(response: dict):
    print("\n--- ORDER RESPONSE ---")
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Exec Qty   : {response.get('executedQty', 'N/A')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price  : {avg_price}")
    print("  ✅ Order placed successfully!")
    print("-" * 22 + "\n")


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None,
):
    try:
        sym = validate_symbol(symbol)
        sid = validate_side(side)
        otype = validate_order_type(order_type)
        qty = validate_quantity(quantity)

        if otype == "LIMIT":
            if not price:
                raise ValidationError("Price is required for LIMIT orders.")
            prc = validate_price(price)
            print_order_summary(otype, sym, sid, qty, prc)
            logger.info(f"Placing LIMIT order: {sym} {sid} qty={qty} price={prc}")
            response = client.place_limit_order(sym, sid, qty, prc)
        else:
            print_order_summary(otype, sym, sid, qty)
            logger.info(f"Placing MARKET order: {sym} {sid} qty={qty}")
            response = client.place_market_order(sym, sid, qty)

        print_order_response(response)
        return response

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        print(f"\n  ❌ Validation Error: {e}\n")
        raise
    except Exception as e:
        logger.error(f"Order failed: {e}")
        print(f"\n  ❌ Order Failed: {e}\n")
        raise
