
from .source_providers.basic_source_provider import BasicSourceProvider


class BaseParser:
    source_provider = None

    def __init__(self, namer=None):
        self.source_provider = BasicSourceProvider()
        self.namer = namer

    def start(self):
        root_keys = self.root_keys()
        for key in root_keys:
            text = self.source_provider.get_page(key, self.namer)
            entity = self.parse(text)
            self.finalize(key, entity)

    def root_keys(self):
        raise NotImplementedError('Should be override')

    def parse(self, text):
        raise NotImplementedError('Should be override')

    def finalize(self, key, entity):
        raise NotImplementedError('Should be override')
