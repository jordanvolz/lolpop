```
class SMTPNotifier(BaseNotifier):
    """
    Class for sending email notifications using the Simple Mail Transfer Protocol (SMTP) protocol.

    Inherits from BaseNotifier.

    Attributes:
        __REQUIRED_CONF__ (dict): A dictionary containing necessary configuration settings for SMTPNotifier.
            "config" (list): A list of required configuration settings for SMTPNotifier:
                "sender_email" (str): Email address of sender.
                "sender_password" (str): Password for sender's email address.
                "smtp_server" (str): SMTP server address.
                "smtp_port" (int): SMTP server port.
                "recipient_email" (str): Email address of recipient.

    Methods:
        notify(msg, level="ERROR", **kwargs) -> None:
            Sends an email notification using the provided message and log level.

            Args:
                msg (str): The body of the email message.
                level (str): The severity level of the notification. Default is "ERROR".
                **kwargs: Additional keyword arguments used if needed.

            Returns:
                None
    """

    __REQUIRED_CONF__ = {
        "config": ["sender_email", "sender_password", "smtp_server", "smtp_port", "recipient_email"]
    }

    def notify(self, msg, level="ERROR", **kwargs):
        """
        Sends an email notification using the provided message and log level.

        Args:
            msg (str): The body of the email message.
            level (str): The severity level of the notification. Default is "ERROR".
            **kwargs: Additional keyword arguments used if needed.

        Returns:
            None
        """

        with smtplib.SMTP(self._get_config("smtp_sever"), self._get_config("smtp_port")) as smtp:

            # Starting TLS encryption
            smtp.starttls()

            # Login using the sender's email address and password
            smtp.login(self._get_config("sender_email"), self._get_config("sender_password"))

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
            smtp.sendmail(self._get_config("sender_email"), self._get_config("recipient_email"), message)
            
            return None