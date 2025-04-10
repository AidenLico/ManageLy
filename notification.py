# Notification system, uses a email address to send an email to a reciever #

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Sender email ##
sender = "test@test.com"
## Get email application password (gmail offers this) ##
password = "abcd efgh ijkl mnop"
## Receiver email ##
receiver = "test@test.com"

# Create the email #
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "ManageLy Notification"

body = "You have a new alert!"
msg.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

    print("Sent")
except Exception as e:
    print(f"Error: {e}")