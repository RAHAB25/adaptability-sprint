"""
# Tracks which attendees are already checked in.
# This is what prevents a duplicate scan from triggering a second print.

checked_in = {}

def is_checked_in(attendee_id):
    return attendee_id in checked_in

def mark_checked_in(attendee_id, name):
    checked_in[attendee_id] = {"name": name, "status": "checked_in"}

def get_status(attendee_id):
    return checked_in.get(attendee_id)
"""

# Tracks check-in status per attendee.
# Status can be: "pending" (job queued, not confirmed yet),
# "checked_in" (print confirmed successful), or
# "print_failed" (print confirmed failed - safe to retry).

checked_in = {}

def get_status(attendee_id):
    return checked_in.get(attendee_id)

def mark_pending(attendee_id, name):
    checked_in[attendee_id] = {"name": name, "status": "pending"}

def mark_result(attendee_id, success):
    if attendee_id in checked_in:
        checked_in[attendee_id]["status"] = "checked_in" if success else "print_failed"