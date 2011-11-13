class PMXProject(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.isFolder = True
    
    def get_full_path(self):
        '''
        Returns the full path of the project
        '''
        return self.path

