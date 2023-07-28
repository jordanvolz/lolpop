# GMailNotifier

The `GMailNotifier` class is a subclass of the `BaseNotifier` class. It provides functionality to send notification emails using the authenticated Gmail API service object.

## Configuration 

### Required Configuration
`GMailNotifier` contains the following required configuration:

- `"gcloud_credentials_file"`: The path to the Google Cloud credentials file.
- `"gcloud_credentials_token"`: The path to the file where the credentials token will be stored.
- `"sender_email"`: The email address of the sender.
- `"recipient_email"`: The email address of the recipient.

### Optional Configuration
`GMailNotifier` has no optional configuration.

### Default Configuration

`GMailNotifier` has no default configuration.


##  Methods


### notify 
 This method sends a notification email using the authenticated Gmail API service object.

```python 
def notify(msg, level="ERROR", *args, **kwargs)
```

   

**Parameters**

- `msg` (str): The message to include in the email.
- `level` (str, optional): The level of the notification. Default is "ERROR".


##  Usage

```python
from lolpop.component import GMailNotifier

config = {
  #insert component configuration
}

# Create an instance of GMailNotifier
notifier = GMailNotifier(conf=config)

# Send a notification email
notifier.notify("This is the notification message")
```
