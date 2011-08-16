'''
Misc functions
'''
def amIRunningForzen():
    '''
    @return: True if program is executed in an executable (exe)
    '''
    return globals().has_key('__file__')