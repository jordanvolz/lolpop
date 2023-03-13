from lolpop.component.notifier.abstract_notifier import AbstractNotifier
import smtplib
from datetime import datetime

class SMTPNotifier(AbstractNotifier): 
    __REQUIRED_CONF__ = {
        "config" : ["sender_email", "sender_password", "smtp_server", "smtp_port", "recipient_email"]
    }

    def __init__(self, conf, *args, **kwargs): 
        #set normal config
        super().__init__(conf, *args, **kwargs)
        

    def notify(self, msg, level="ERROR", **kwargs): 
        with smtplib.SMTP(self.email_config.get("smtp_sever"), self.email_config.get("smtp_port")) as smtp:
            # Starting TLS encryption
            smtp.starttls()
            
            # Login using the sender's email address and password
            smtp.login(self.email_config.get("sender_email"), self.email_config.get("sender_password"))
            
            message = """
            To: %s
            From: %s
            Subject: [%s] %s 
            Date: %s 

            %s
            """ %(
                self.email_config.get("recipient_email"),
                self.email_config.get("sender_email"),
                level,
                "Notification from MLOps Jumpstart Workflow!",
                datetime.utcnow().strftime(" %d/%M/%y %H:%M:%s"),
                msg
            )
            # Sending the message
            smtp.sendmail(sender_email, receiver_email, message)