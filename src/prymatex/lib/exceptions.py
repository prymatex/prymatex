
class UnsupportedPlatformError(Exception):
    RETURN_VALUE = 1
    '''
    Some code must be ported if this exception is rised
    '''
    pass

class AlreadyRunningError(Exception):
    RETURN_VALUE = 10
    
class ConfigNotFound(Exception):
    RETURN_VALUE = 15