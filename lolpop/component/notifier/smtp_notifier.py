from lolpop.component.notifier.abstract_notifier import AbstractNotifier

#mainly to be used for development/testing purposes... when you don't actually want to notify
class StdOutNotifier(AbstractNotifier): 
    __REQUIRED_CONF__ = {
        "config" : []
    }

    def __init__(self, conf, *args, **kwargs): 
        #set normal config
        super().__init__(conf, *args, **kwargs)
        

    def notify(self, msg, level="ERROR", **kwargs): 
        print(msg)