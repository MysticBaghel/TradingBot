# Trading Bot — Binance Futures Testnet

A clean Python CLI tool to place **MARKET** and **LIMIT** orders on Binance Futures Testnet (USDT-M).

---

## Setup

### 1. Clone / unzip the project

```bash
cd trading_bot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Register at [https://testnet.binancefuture.com](https://testnet.binancefuture.com) and generate your API Key + Secret.

Then create a `.env` file:

```bash
cp .env.example .env
# Edit .env and fill in your keys
```

---

## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 30000
```

### All CLI flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--symbol` | `-s` | ✅ | Trading pair (e.g. BTCUSDT) |
| `--side` | | ✅ | BUY or SELL |
| `--type` | `-t` | ✅ | MARKET or LIMIT |
| `--quantity` | `-q` | ✅ | Quantity to trade |
| `--price` | `-p` | LIMIT only | Limit price |

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper (REST + HMAC signing)
│   ├── orders.py          # Order placement logic + formatted output
│   ├── validators.py      # Input validation with clear error messages
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Assumptions

- Uses Binance **Futures Testnet** only (`https://testnet.binancefuture.com`)
- All orders use USDT-M perpetual futures
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled)
- API calls are signed using HMAC-SHA256 as required by Binance

---

## Logs

Each run creates a timestamped log file in the `logs/` directory, e.g.:

```
logs/trading_bot_20240325_153045.log
```

Logs include: request params, full API response, validation errors, and network failures.
