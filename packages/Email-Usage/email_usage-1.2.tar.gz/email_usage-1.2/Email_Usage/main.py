import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_verification(appname, clientpass, clientemail, emailtosend, text=True):

    # Email Structure
    if text is True:
        subject = f"Email Verification for: {appname}"
        secured_code = random.randint(000000, 999999)
        body = f"""
            <html>
            <body>
                <h1>{appname}</h1>
                <p>You have requested a verification code for {appname}.</p>
                <p>Your digital verification code is <strong>{secured_code}</strong></p>
            </body>
            </html>
            """

        message = MIMEMultipart()
        message["From"] = clientemail
        message["To"] = emailtosend
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))


    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(clientemail, clientpass)


        server.sendmail(clientemail, emailtosend, message.as_string())
        print("Email sent successfully!")
        return secured_code

        server.quit()
    except Exception as e:
        print(f"Error occurred: {e}")