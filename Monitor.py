import time
import win32evtlogutil
import win32evtlog
import win32con

# Define the name of your application's log file, source names, and event IDs
app_log_name = "Application"
app_source_names = ["Application Error", "Windows Error Reporting"]
app_event_ids = [1000, 1001]  # Event IDs for application error

# Function to check for recent crash events
def check_for_crash():
    # Open the event log
    hand = win32evtlog.OpenEventLog(None, app_log_name)

    # Check if the event log was successfully opened
    if hand is None:
        print("Failed to open event log")
        return False

    # Get the number of events in the log
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand, flags, 0)

    # Check if events were successfully retrieved
    if events is None:
        print("Failed to read events from event log")
        return False

    # Iterate over each event
    for event in events:
        # print(f"Event Source: {event.SourceName}, Event ID: {event.EventID}, Event Description: {' '.join(event.StringInserts) if isinstance(event.StringInserts, list) else event.StringInserts}")

        # Check if the event source and event ID match
        if event.SourceName in app_source_names and event.EventID in app_event_ids:
            return True  # Return True if any matching event found

    return False  # Return False if no matching event found


# Main loop
while True:
    print("Monitoring!!!")
    if check_for_crash():
        print("Application has crashed!")

    time.sleep(30)
