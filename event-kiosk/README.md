# Event Kiosk

A small Flask demo for an event check-in flow where attendee badge printing is handled asynchronously through a queue and a webhook confirmation.

## Overview

The app simulates a real event kiosk:

- A visitor scans or enters an attendee ID.
- The kiosk marks the attendee as `pending`.
- A background worker sends a print job to a simulated vendor.
- The vendor webhook confirms the print result.
- The attendee becomes `checked_in` only after confirmation.

This is a realistic example of a workflow where a backend action is not immediately complete and must be reconciled after an external system responds.

## How it works

- `server.py` runs the Flask app and exposes the kiosk API.
- `checkin_store.py` stores attendee status in memory and tracks states such as `pending`, `checked_in`, and `print_failed`.
- `printer_vendor.py` simulates the badge printer API and can randomly fail a print job.
- `static/index.html` renders the check-in dashboard and logs activity for the demo.

## Main endpoints

- `GET /` — dashboard UI
- `GET /attendees` — returns attendee metadata
- `GET /checkin/<attendee_id>` — starts the check-in flow
- `GET /status/<attendee_id>` — returns the current attendee status
- `POST /webhook/print-complete` — receives the print result from the vendor
- `POST /reset` — clears the demo state

## Typical flow

1. Open the kiosk dashboard at `http://127.0.0.1:8001/`.
2. Scan an attendee ID or enter one manually.
3. The app marks the attendee as `pending` and pushes a print job onto a queue.
4. The background worker calls the simulated printer vendor.
5. The printer replies through `/webhook/print-complete`.
6. The kiosk updates the attendee to `checked_in` or `print_failed`.

## Run locally

From the project folder:

```bash
cd event-kiosk
python -m venv .venv
.\.venv\Scripts\activate.ps1
pip install flask requests
python server.py
```

Then open:

```text
http://127.0.0.1:8001/
```

## Notes

- The app uses an in-memory store, so state resets when the server restarts.
- The demo intentionally includes flaky print success behavior to simulate real-world vendor failures.
- The UI can be used to reset the demo and re-run the check-in sequence.
