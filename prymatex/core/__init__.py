
#TODO: Setup qt
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

'''
Misc functions
'''
def amIRunningForzen():
    '''
    @return: True if program is executed in an executable (exe)
    '''
    return globals().has_key('__file__')