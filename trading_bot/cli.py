#!/usr/bin/env python3
"""
Trading Bot CLI — Binance Futures Testnet
Place MARKET and LIMIT orders from the command line.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import ValidationError

load_dotenv()


def get_credentials():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        print("\n  ❌ Missing API credentials.")
        print("  Set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.\n")
        sys.exit(1)
    return api_key, api_secret


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet — Place MARKET and LIMIT orders",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type", "-t",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity", "-q",
        required=True,
        help="Quantity to trade (e.g. 0.001)",
    )
    parser.add_argument(
        "--price", "-p",
        default=None,
        help="Limit price (required for LIMIT orders)",
    )
    return parser


def main():
    log_file = setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    print(f"\n  📄 Logs: {log_file}")

    api_key, api_secret = get_credentials()
    client = BinanceClient(api_key, api_secret)

    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except (ValidationError, Exception):
        sys.exit(1)


if __name__ == "__main__":
    main()
