import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "aiden.lico@gmail.com"
password = "hzza xyzn apxr bdgi"
receiver = "niyave4659@noroasis.com"

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