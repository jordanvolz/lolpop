from lolpop.component.notifier.base_notifier import BaseNotifier

#mainly to be used for development/testing purposes... when you don't actually want to notify


class StdOutNotifier(BaseNotifier):
    __REQUIRED_CONF__ = {
        "config": []
    }

    def notify(self, msg, level="ERROR", **kwargs):
        print(msg)