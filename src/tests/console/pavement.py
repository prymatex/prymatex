@task
def ui():
    sh('pyuic4 -o qt_ipython.py qt_ipython.ui')
    
    
