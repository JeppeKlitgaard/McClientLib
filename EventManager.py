class Event(list):
    """This objects represents an event.
    It simply iterates thru a list of handlers once it's fired.

    If a handler raises StopIteration,
    it will not fire the rest of the handlers.

    Supports list methods, and the following:


    Event.clear() -> Clears list of handlers.

    Event.add_handler(handler) -> Adds a handler.
        Same as Event.append(handler), except it checks if the handler is sane.

    Event.remove_handler(handler) -> Removes a handler.
        Same as Event.remove(handler)

    Event.fire(*args, **kwargs) -> Fires event, by iterating thru handlers.
        Executing each handler with *args and **kwargs.

    Event(*args, **kwargs) -> Same as Event.fire(*args, **kwargs)

    Event.eventmanager => The EventManager for event.

    Event.add_name(name) -> Adds an "alias". Can also be a list of names.

    Event.remove_name(name) -> Removes an "alias". Can also be a list of names.
    """
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._eventmanager = None
        self.names = set()

    def clear(self):
        del self[:]
        return True

    def add_handler(self, handler):
        if not hasattr(handler, "__call__"):
            raise TypeError("'%s' is not callable." % handler)

        self.append(handler)

    def remove_handler(self, handler):
        self.remove(handler)

    def fire(self, *args, **kwargs):
        if self.eventmanager:
            self.eventmanager.got_event(self.names, *args, **kwargs)

        for handler in self:
            try:
                handler(*args, **kwargs)
            except StopIteration:
                break

    def __call__(self, *args, **kwargs):
        self.fire(*args, **kwargs)

    def add_name(self, name):
        if type(name) == list:
            for x in name:
                self.add_name(x)
        else:
            self.names.add(name)
            if self.eventmanager:
                self.eventmanager[name] = self
                return True
            return False

    def remove_name(self, name):
        if type(name) == list:
            for x in name:
                self.remove_name(x)
        else:
            self.names.remove(name)
            del self.eventmanager[name]

    @property
    def eventmanager(self):
        return self._eventmanager

    @eventmanager.setter
    def eventmanager(self, eventmanager):
        self._eventmanager = eventmanager
        for name in self.names:
            self.add_name(name)

    @eventmanager.deleter
    def eventmanager(self):
        for name in self.names:
            if self.eventmanager[name] is self:
                self.remove_name(name)
        self._eventmanager = None


class EventManager(dict):
    def __init__(self, *args, **kwargs):
        super(EventManager, self).__init__(*args, **kwargs)
        self.got_event = Event()

    def __setitem__(self, key, value):
        super(EventManager, self).__setitem__(key, value)

        if self[key].eventmanager is not self:
            self[key].eventmanager = self
