from lolpop.component.notifier.base_notifier import BaseNotifier
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime 
import os

#note, you need to set up your google account to allow gmail api access and generate a credentials json file. 
#some instructions on that can be found here if you are lost: 
#https://developers.google.com/gmail/api/quickstart/python
#https://mailtrap.io/blog/python-send-email-gmail/#How-to-send-an-email-with-Python-via-Gmail-API
#
#Note: this works but requires browser auth due to oauth2 for the initial authorization. 
#Not sure if there's a more streamlined version to do this w/ gmail. May have to just use generic smtp server/SMTPNotificer.
class GMailNotifier(BaseNotifier): 
    __REQUIRED_CONF__ = {
        "config" : ["gcloud_credentials_file", "gcloud_credentails_token", "sender_email", "receipient_email"]
    }

    def __init__(self, *args, **kwargs): 
        #set normal config
        super().__init__(*args, **kwargs)
        creds_file = self._get_config("gcloud_credentials_file")
        token_file = self._get_config("gcloud_credentials_token")
        SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        service = build('gmail', 'v1', credentials=creds)
        self.service = service

    def notify(self, msg, level="ERROR", **kwargs): 
        message = MIMEText(msg)
        #message['from'] = self.email_config.get("sender_email")
        message['to'] = self._get_config("recipient_email")
        message['subject'] = "Notification from MLOps Jumpstart Workflow"
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            message = (self.service.users().messages().send(userId=self._get_config("sender_email"),body=create_message).execute())
            self.log('Sent notification email: %s' %message)
        except Exception as error:
            self.log('An error occurred: %s' %error, "ERROR")
            message = None