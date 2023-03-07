import smtplib
import yaml

def send_email(subject, body, *to_address):
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    smtp_server = config['SMTP_SERVER']
    smtp_port = config['SMTP_PORT']
    email_address = config['EMAIL_ADDRESS']
    email_password = config['EMAIL_PASSWORD']

    message = (f'From: {email_address}\nTo:{", ".join(to_address)}'
                f'\nSubject: {subject}\n\n{body}')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, to_address, message)
            server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Error: Could not authenticate with SMTP server.")
    except smtplib.SMTPException as e:
        print(f"Error: {e}")
