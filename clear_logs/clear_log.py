import win32evtlog

def clear_application_logs():
    try:
        # Open the Application Event Log
        hand = win32evtlog.OpenEventLog(None, "Application")

        # Clear all the events in the Application Event Log
        win32evtlog.ClearEventLog(hand, None)

        # Close the Event Log handle
        win32evtlog.CloseEventLog(hand)
        print("Application logs cleared successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clear_application_logs()

    # Wait for user input to exit
    input("Press Enter to exit...")
