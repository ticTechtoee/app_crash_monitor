import time
import win32evtlogutil
import win32evtlog
import win32con
# For Email Module

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ

# Email Setup


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

GET_SENDER_EMAIL = env('SENDER_EMAIL')
GET_RECEIVER_EMAIL = env('RECEIVER_EMAIL')
GET_PASSWORD = env('EMAIL_PASSWORD')

# Set up the email addresses and SMTP server
sender_email = GET_SENDER_EMAIL
receiver_email = GET_RECEIVER_EMAIL
password = GET_PASSWORD
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_script_email(email_subject, email_message):
    try:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = email_subject

        # Add body to email
        body = email_message
        message.attach(MIMEText(body, "plain"))

        # Log in to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Quit SMTP server
        server.quit()

        return True
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False




# Define the name of your application's log file, source names, and event IDs
app_log_name = "Application"
app_source_names = ["Application Error", "Windows Error Reporting"]
app_event_ids = [1000, 1001]  # Event IDs for application error

# Function to check for recent crash events
def check_for_crash():
    try:
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
            # Check if the event source and event ID match
            if event.SourceName in app_source_names and event.EventID in app_event_ids:
                return True  # Return True if any matching event found

        return False  # Return False if no matching event found
    except Exception as e:
        print("An error occurred while checking for crash:", str(e))
        return False


    # Clear log after reading

def clear_event_log(log_name):
    try:
        # Open the event log
        hand = win32evtlog.OpenEventLog(None, log_name)

        # Check if the event log was successfully opened
        if hand is None:
            print(f"Failed to open event log '{log_name}'")
            return False

        # Clear the event log
        if not win32evtlog.ClearEventLog(hand, None):
            print(f"Failed to clear event log '{log_name}'")
            return False

        print(f"Event log '{log_name}' cleared successfully")
        return True
    except Exception as e:
        print("An error occurred while clearing the event log:", str(e))
        return False



# Main loop
while True:
    print("Monitoring!!!")
    if check_for_crash():
        print("Application has crashed!")
        send_script_email("Crash Report", "Your Application has crashed")
        clear_event_log("Application")

    time.sleep(30)
