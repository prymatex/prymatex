#!/usr/bin/env python

class Settings(dict):
    def __init__(self, name, settings):
        super(Settings, self).__init__(settings)
        self._name = name
        # Callbacks
        self._callbacks = {}

    def name(self):
        return self._name

    def set(self, name, value):
        self[name] = value
        for callback in self._callbacks.get(name, []):
            callback(value)

    def get(self, name, default=None):
        return super(Settings, self).get(name, default)

    def erase(self, name):
        if name in self:
            del self[name]

    def has(self, name):
        return name in self.items

    def add_callback(self, name, callback):
        # Add callback
        callbacks = self._callbacks.setdefault(name, [])
        if callback not in callbacks:
            callbacks.append(callback)

    def remove_callback(self, name, callback=None):
        if callback:
            callbacks = self._callbacks.setdefault(name, [])
            if callback in callbacks:
                callbacks.remove(callback)
        elif name in self._callbacks:
            del self._callbacks[name]
        
