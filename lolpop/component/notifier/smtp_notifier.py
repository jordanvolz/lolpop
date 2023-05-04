from lolpop.component.notifier.base_notifier import BaseNotifier
import smtplib
from datetime import datetime


class SMTPNotifier(BaseNotifier):
    __REQUIRED_CONF__ = {
        "config": ["sender_email", "sender_password", "smtp_server", "smtp_port", "recipient_email"]
    }

    def notify(self, msg, level="ERROR", **kwargs):
        with smtplib.SMTP(self._get_config("smtp_sever"), self._get_config("smtp_port")) as smtp:
            # Starting TLS encryption
            smtp.starttls()

            # Login using the sender's email address and password
            smtp.login(self._get_config("sender_email"),
                       self._get_config("sender_password"))

            message = """
            To: %s
            From: %s
            Subject: [%s] %s 
            Date: %s 

            %s
            """ % (
                self._get_config("recipient_email"),
                self._get_config("sender_email"),
                level,
                "Notification from lolpop!",
                datetime.utcnow().strftime(" %d/%M/%y %H:%M:%s"),
                msg
            )
            # Sending the message
            smtp.sendmail(self._get_config("sender_email"),
                          self._get_config("recipient_email"), message)
