import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ACCOUNT = "aliahmedfree62@gmail.com"
APP_PASSWORD = "yxav fzwl denm aeko"  # Generate from Google Account Security

# Email content
# receiver_email = "developerumair44@gmail.com"
receiver_email = "aliahmedfree62@gmail.com"
subject = "Hello 2 from Python"
body = "This is a second test email sent using Python and Gmail SMTP."

# Create MIME object
msg = MIMEMultipart()
msg["From"] = EMAIL_ACCOUNT
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

# Connect and send email
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(EMAIL_ACCOUNT, APP_PASSWORD)
    server.sendmail(EMAIL_ACCOUNT, receiver_email, msg.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
finally:
    server.quit()
