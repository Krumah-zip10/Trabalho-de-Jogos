class EventHandler:
    def __init__(self):
        self.observers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.observers:
            self.observers[event_type] = []
        self.observers[event_type].append(callback)

    def notify(self, event_type, data=None):
        for callback in self.observers.get(event_type, []):
            callback(data)