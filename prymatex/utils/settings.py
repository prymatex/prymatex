#!/usr/bin/env python

import sys
from . import json

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

    def erase(self, name):
        if name in self:
            del self[name]

    def reload(self, attrs):
        for name, value in attrs.items():
            self.set(name, value)

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
        
    def write(self, path):
        json.write_file(self, path)

    @staticmethod
    def get_data(path):
        return json.read_file(path) or {}
