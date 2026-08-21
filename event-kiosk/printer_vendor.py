import time
import random

# Simulates the vendor's SYNCHRONOUS print API.
# In real life this would be an HTTP call to their server that we wait on.
def print_badge(attendee_name):
    print(f"Sending print job for {attendee_name} to vendor...")
    time.sleep(1)  # simulate the network/printing delay
    success = random.random() > 0.1  # ~90% success rate, like a real flaky printer
    return {"success": success, "attendee": attendee_name}