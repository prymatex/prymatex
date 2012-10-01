#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MultiListsDict(dict):
    """
    A subclass of dictionary customized to handle multiple lists for the same key.

    >>> d = MultiListsDict({'name': ['Dylan', 'Natalia']})
    >>> d['name']
    ['Dylan', 'Natalia']
    >>> d.update({'name': ['Diego']})
    >>> d['name']
    ['Dylan', 'Natalia', 'Diego']
    """
    def lists(self):
        """Returns a list of (key, list) pairs."""
        return super(MultiListsDict, self).items()
        
    def update(self, *args, **kwargs):
        """
        update() extends existing key lists.
        Also accepts keyword args.
        """
        
        if args:
            other_dict = args[0]
            if isinstance(other_dict, MultiListsDict):
                for key, value_list in other_dict.lists():
                    self.setdefault(key, []).extend(value_list)
            else:
                try:
                    for key, value in other_dict.items():
                        self.setdefault(key, []).extend(value)
                except TypeError:
                    raise ValueError("MultiListsDict.update() takes either a MultiListsDict or dictionary")
        for key, value in kwargs.iteritems():
            self.setdefault(key, []).extend(value)
