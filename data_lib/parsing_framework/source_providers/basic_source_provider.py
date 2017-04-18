
from ..source_storages.basic_source_storage import BasicSourceStorage as SourceStorage
from ..source_loaders.urllib import UrllibDownloader as SourceLoader


class BasicSourceProvider:
    def __init__(self, source_storage_class=SourceStorage, source_loader_class=SourceLoader):
        self.source_storage = source_storage_class()
        self.source_loader = source_loader_class()

    def get_page(self, key, namer):
        filename = namer.get_filename(key)
        if self.source_storage.is_file_exists(filename):
            text = self.source_storage.read_file(filename)
            print('%s =>' % filename)
        else:
            url = namer.get_url(key)
            text = self.source_loader.get_as_text(url)
            self.source_storage.write_file(filename, text)
            print('%s => %s' % (url, filename))
        return text
