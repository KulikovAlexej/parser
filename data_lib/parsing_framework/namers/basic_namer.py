
class BasicNamer:
    def __init__(self, get_filename, get_url):
        self.get_filename = get_filename
        self.get_url = get_url

    def get_filename(self, key):
        raise NotImplementedError('Should be override')

    def get_url(self, key):
        raise NotImplementedError('Should be override')
