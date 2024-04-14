import time
import win32evtlog
import win32evtlogutil
import win32con
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ctypes
import environ
import sys
from datetime import datetime  # Import datetime module

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Email configuration
sender_email = env('SENDER_EMAIL')
receiver_email = env('RECEIVER_EMAIL')
password = env('EMAIL_PASSWORD')
smtp_server = "smtp.gmail.com"
smtp_port = 587

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print("An error occurred while checking admin privileges:", str(e))
        return False

def send_email(subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email notification sent successfully")
        return True
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False

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

def check_for_crash():
    try:
        hand = win32evtlog.OpenEventLog(None, "Application")
        if hand is None:
            print("Failed to open event log 'Application'")
            return False

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        if events is None:
            print("Failed to read events from event log 'Application'")
            return False

        for event in events:
            if event.SourceName in ["Application Error", "Windows Error Reporting"] and event.EventID in [1000, 1001]:
                # event_time = datetime.fromtimestamp(event.TimeGenerated)  # Convert to Python datetime object
                event_description = event.StringInserts
                return event_description

        return None, None
    except Exception as e:
        print("An error occurred while checking for crash:", str(e))
        return None, None

# Main loop
while True:
    print("Monitoring!!!")
    crash_description = check_for_crash()
    if crash_description:
        print("Application has crashed!")
        email_subject = "Application Crash Report"
        email_body = f"Application has crashed!\n\nTime:\nDescription: {crash_description}"
        if send_email(email_subject, email_body):
            print("Email sent successfully")
            clear_application_logs()
        else:
            print("Failed to send email notification")

    time.sleep(30)
