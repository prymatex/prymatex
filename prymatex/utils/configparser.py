try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class ConfigParser(configparser.ConfigParser):
    """Can get options() without defaults"""
    def options(self, section, no_defaults=False, **kwargs):
        if no_defaults:
            try:
                return list(self._sections[section].keys())
            except KeyError:
                raise NoSectionError(section)
        else:
            return super().options(section, **kwargs)