import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.ehlo()
s.starttls()
s.ehlo()
# Authentication
s.login(os.getenv("EMAIL_SENDER"), os.getenv("APP_PASSWORD"))
# message to be sent
message = "How are you?"
# sending the mail
s.sendmail(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_RECEIVER"), message)
# terminating the session
s.quit()
