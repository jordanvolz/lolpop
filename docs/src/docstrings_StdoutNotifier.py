class StdOutNotifier(BaseNotifier):
    """
    Notifies the user of error messages through standard output.

    This class inherits from BaseNotifier.

    """
    __REQUIRED_CONF__ = {
        "config": []
    }

    def notify(self, msg, level="ERROR", **kwargs):
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