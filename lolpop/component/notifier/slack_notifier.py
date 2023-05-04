from lolpop.component.notifier.base_notifier import BaseNotifier


class SlackNotifier(BaseNotifier): 
    __REQUIRED_CONF__ = {
        "config" : ["gcloud_credentials_file"]
    }


    def notify(self, msg, level="ERROR", **kwargs): 
        pass
    # import os
    # from slack_sdk import WebClient
    # from slack_sdk.errors import SlackApiError

    # # Your Slack API token
    # SLACK_API_TOKEN = "xoxb-your-token"

    # # Slack channel to send the message to
    # SLACK_CHANNEL = "#your-channel"

    # # The message to be sent
    # SLACK_MESSAGE = "Your message"

    # client = WebClient(token=SLACK_API_TOKEN)

    # try:
    #     response = client.chat_postMessage(
    #         channel=SLACK_CHANNEL,
    #         text=SLACK_MESSAGE
    #     )
    #     print(response)
    # except SlackApiError as e:
    #     print("Error sending message: {}".format(e))