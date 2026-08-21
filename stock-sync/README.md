# Stock Sync

A Flask-based stock lookup service that serves product inventory from a local JSON cache and accepts webhook updates from a vendor or upstream system.

## Overview

This project demonstrates a simple inventory synchronization flow:

- A client queries product stock by SKU.
- The server reads the value from a cached store.
- An upstream system can push inventory updates through an HTTP webhook.
- The cache is updated and immediately available to future queries.

This makes the app a lightweight example of a stock sync service that exposes both a read endpoint and an update endpoint.

## How it works

- `server.py` hosts the Flask app and exposes the API routes.
- `stock_cache.py` loads and saves the cache to `cache.json`.
- `warehouse_api.py` contains an older polling-based implementation kept as a reference; it is no longer used in the active workflow.
`warehouse_api.py` on a timer; deprecated after the Day 4 webhook pivot, kept for reference only.
- `static/index.html` provides a browser UI for looking up SKUs and simulating incoming webhook updates.


## Main endpoints

- `GET /` — dashboard UI
- `GET /stock/<sku>` — returns the cached stock record for a SKU
- `POST /webhook/stock-update` — accepts an inventory update payload and refreshes the cache

## Example payload

```json
{
  "sku": "NR-1042",
  "name": "Cast Iron Skillet, 10 inch",
  "stock": 24
}
```

## Run locally

From the project folder:

```bash
cd stock-sync
python -m venv .venv
.\.venv\Scripts\activate.ps1
pip install flask flask-cors
python server.py
```

Then open:

```text
http://localhost:8000/
```

## Demo usage

1. Open the dashboard in the browser.
2. Search for a SKU such as `NR-1042`.
3. The app reads the current value from the local cache.
4. Use the simulated webhook form to push a new stock count.
5. Query the same SKU again to confirm the cache was updated.

## Notes

- The app stores state in `cache.json`, so it persists across restarts.
- The current design is intentionally simple and meant for a sprint demo rather than production-grade inventory syncing.
- `warehouse_api.py` is retained as a historical reference for the earlier polling-based approach, not the active webhook flow.
