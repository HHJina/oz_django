from config import settings

def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email,list) else [to_email]

    send_email(subject, message, settings.EMAIL_HOST_USER, to_email)