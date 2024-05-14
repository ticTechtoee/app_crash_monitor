import time
import win32evtlog
import win32evtlogutil
import win32con
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ctypes
import environ
from datetime import datetime, timedelta
import os
import subprocess
import sys
# Constants
CHECK_INTERVAL = 30  # seconds
# Initialize environment variables
env = environ.Env()
environ.Env.read_env()
# Email configuration
CUSTOMER_NAME = env('CUSTOMER_NAME')
SENDER_EMAIL = env('SENDER_EMAIL')
RECEIVER_EMAIL = env('RECEIVER_EMAIL')
EMAIL_PASSWORD = env('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SET_RESTART_TIME = env('RESTART_TIME')
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print("An error occurred while checking admin privileges:", str(e))
        return False
def send_email(subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        server.quit()
        print("Email Sending in progress")
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
        print(f"An error occurred while clearing application logs: {e}")
def check_for_crash():
    try:
        hand = win32evtlog.OpenEventLog(None, "Application")
        if hand is None:
            print("Failed to open event log 'Application'")
            return None
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events is None:
            print("Failed to read events from event log 'Application'")
            return None
        for event in events:
            if event.SourceName in ["Application Error", "Windows Error Reporting"] and event.EventID in [1000, 1001]:
                event_description = event.StringInserts
                application_name = ""
                for desc in event_description:
                    if "Application Name:" in desc:
                        application_name = desc.split(":")[1].strip()
                        break
                return application_name, event_description
        return None
    except Exception as e:
        print("An error occurred while checking for crash:", str(e))
        return None
def print_current_time_minus_30_seconds():
    current_time = datetime.now()
    modified_time = current_time - timedelta(seconds=CHECK_INTERVAL)
    formatted_time = modified_time.strftime("%d-%m-%Y %I:%M:%S %p")
    return formatted_time
def main():
    # Set console title
    ctypes.windll.kernel32.SetConsoleTitleW("sync-assistant")
    # Check if saved path exists
    saved_path = read_path_from_file()
    if saved_path and os.path.exists(saved_path):
        print("Using saved path from 'application_path.txt':", saved_path)
        while True:
            event_time = print_current_time_minus_30_seconds()
            print(f"EasySales Sync Program - OK!\n{event_time}")
            crash_info = check_for_crash()
            if crash_info:
                print("Application has crashed!")
                application_name, crash_description = crash_info
                print(f"Application Name: {crash_description[5]}")
                if crash_description[5] == "EasySales.exe":
                    email_subject = "Application Crash Report"
                    email_body = f"Mr {CUSTOMER_NAME}\nApplication has crashed!\n\nTime: {event_time}\nApplication Name: {application_name}\nDescription: {crash_description}"
                    if send_email(email_subject, email_body):
                        print(f"Email has been sent at {event_time}.")
                    else:
                        print("Failed to send email notification")
                    clear_application_logs()
                    time.sleep(int(SET_RESTART_TIME))
                    start_application(saved_path)
                    continue
                else:
                    clear_application_logs()
                    continue
            time.sleep(CHECK_INTERVAL)
    else:
        # Ask the user to provide the complete path of the application
        path = input("Please provide the complete path of the application: ")
        # Check if the provided path ends with '.exe'
        if path.endswith('.exe') and os.path.exists(path):
            print("Path exists. You provided:", path)
            # Save the path to a text file
            save_path_to_file(path)
            print("Path saved to 'application_path.txt'.")
            # Start monitoring for crashes
            main()
        else:
            print("Please provide the path of the application executable (.exe) and ensure it exists.")
def save_path_to_file(path):
    with open("application_path.txt", "w") as file:
        file.write(path)
def read_path_from_file():
    if os.path.exists("application_path.txt"):
        with open("application_path.txt", "r") as file:
            return file.read().strip()
    return None
def start_application(path):
    if sys.platform == 'win32':
        # On Windows, use ShellExecute to run with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", path, None, None, 1)
    else:
        # On Unix-like systems, use sudo to run with admin rights
        subprocess.call(['sudo', 'xdg-open', path])
if __name__ == "__main__":
    main()
