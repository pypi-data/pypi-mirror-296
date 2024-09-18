import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_verification(subject, emailtosend, clientemail, clientpass, host="smtp.gmail.com", port=587, text=True):

    # Email Structure
    if text is True:
        subject = f"Email Verification for: {subject}"
        secured_code = random.randint(000000, 999999)
        body = f"""
            <html>
            <body>
                <h1>{subject}</h1>
                <p>You have requested a verification code for {subject}.</p>
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
        server = smtplib.SMTP(host=host, port=port)
        server.starttls()
        server.login(clientemail, clientpass)

        server.sendmail(clientemail, emailtosend, message.as_string())
        server.quit()

        return secured_code

    except smtplib.SMTPAuthenticationError:
        print('Invalid Email/App password, check again')

    except smtplib.SMTPRecipientsRefused:
        print('Recipient Refused Error')

    except smtplib.SMTPSenderRefused:
        print("Authentication error. Client not verified")

    except smtplib.SMTPConnectError:
        print("Couldn't establish connection to SMTP")

    except smtplib.SMTPServerDisconnected:
        print("SMTP server down or have problem connecting")

    except smtplib.SMTPNotSupportedError:
        print("SMTP not supported by server try choosing manually using 'port='")
    except Exception as e:
        print(f'unknown error occourd: {e}')



def simplesend(emailtosend, clientemail, clientpass, text, host='smtp.gmail.com', port=587):
    try:
        server = smtplib.SMTP(host=host, port=port)
        server.starttls()
        server.login(clientemail, clientpass)
        server.sendmail(clientemail, emailtosend, text)
        server.quit()
        return "sent successfully"
    
    
    except smtplib.SMTPAuthenticationError:
        print('Invalid Email/App password, check again')

    except smtplib.SMTPRecipientsRefused:
        print('Recipient Refused Error')

    except smtplib.SMTPSenderRefused:
        print("Authentication error. Client not verified")

    except smtplib.SMTPConnectError:
        print("Couldn't establish connection to SMTP")

    except smtplib.SMTPServerDisconnected:
        print("SMTP server down or have problem connecting")

    except smtplib.SMTPNotSupportedError:
        print("SMTP not supported by server try choosing manually using 'port='")
    except Exception as e:
        print(f'unknown error has occourd: {e}')
