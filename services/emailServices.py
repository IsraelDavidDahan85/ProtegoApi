from utils.config import settings as config
from flask_mail import Mail, Message
from app import mail

class EmailServices:

    @staticmethod
    def sendEmail(email, subject, message):
        msg = Message(
            subject=subject,
            recipients=[email],
            body=message,
            sender=config['mail']['username']  # Use the Ethereal email as sender
        )
        msg.body = message
        mail.send(msg)
