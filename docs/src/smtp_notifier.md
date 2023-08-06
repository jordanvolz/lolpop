# SMTPNotifier 

The `SMTPNotifier` class is a Python class that inherits from the `BaseNotifier` class. It provides the functionality to send email notifications using the Simple Mail Transfer Protocol (SMTP).

## Configuration 

### Required Configuration
`StdOutNotifier` contains the following required configuration:

- `sender_email`: The email address of the sender.
- `sender_password`: The password for the sender's email account.
- `smtp_server`: The SMTP server address.
- `smtp_port`: The port number for the SMTP server.
- `recipient_email`: The email address of the recipient.

### Optional Configuration
`StdOutNotifier` has no optional configuration.

### Default Configuration

`StdOutNotifier` has no default configuration.

## Class Methods

### notify 
This method sends an email notification using the provided message and log level.

```python 
def notify(self, msg, level="ERROR", *args, **kwargs)
```



**Parameters**

- `msg (str)`: The body of the email message.
- `level (str)`: The severity level of the notification. Default is "ERROR".
- `**kwargs`: Additional keyword arguments used if needed.


## Usage

```python
from lopop.component import SMTPNotifier 

config= {
    #insert component configuration
}

notifier = SMTPNotifier(conf=config )
msg = "This is a test email notification."
notifier.notify(msg, level="INFO")
```
