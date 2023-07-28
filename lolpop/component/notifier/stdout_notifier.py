from lolpop.component.notifier.base_notifier import BaseNotifier

#mainly to be used for development/testing purposes... when you don't actually want to notify
class StdOutNotifier(BaseNotifier):
    __REQUIRED_CONF__ = {
        "config": []
    }

    def notify(self, msg, level="ERROR", *args, **kwargs):
        """
        Print the error message to standard output.

        Args:
        - msg (str): the message to be printed to standard output
        - level (str): the level of the message (default: "ERROR")
        - **kwargs: additional keyword arguments that may be ignored

        Returns:
        - None

        """
        print(msg)