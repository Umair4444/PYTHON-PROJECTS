import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

load_dotenv()
email_account = os.getenv('EMAIL_ACCOUNT')
app_password = os.getenv('APP_PASSWORD')

print(email_account)

# Gmail IMAP server
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = email_account
APP_PASSWORD = app_password  # Generate from Google Account Security

# Connect to Gmail
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
mail.select("inbox")

# Search emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# Fetch the latest email
latest_email_id = email_ids[-1]
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
msg = email.message_from_bytes(msg_data[0][1])

# Decode subject
subject, encoding = decode_header(msg["Subject"])[0]
if isinstance(subject, bytes):
    subject = subject.decode(encoding if encoding else "utf-8")

print("From:", msg.get("From"))
print("Subject:", subject)
