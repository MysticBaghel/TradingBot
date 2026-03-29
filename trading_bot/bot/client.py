import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.info(f"POST {url} | params: { {k: v for k, v in signed.items() if k != 'signature'} }")
        try:
            response = self.session.post(url, data=signed, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            raise

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": quantity,
        }
        return self._post("/fapi/v1/order", params)

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC",
        }
        return self._post("/fapi/v1/order", params)
