class EventManager:
    def __init__(self):
        self._listeners = []
    
    def subscribe(self, listener):
        self._listeners.append(listener)

    def notify(self, lines):
        for listener in self._listeners:
            listener.update(lines)