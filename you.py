import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import environ

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

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Email Script Testing"

# Add body to email
body = "This is the body of the email."
message.attach(MIMEText(body, "plain"))

# Log in to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, password)

# Send email
server.sendmail(sender_email, receiver_email, message.as_string())

# Quit SMTP server
server.quit()
