
import urllib
import urllib.request
from .basic_source_loader import BasicSourceLoader


class UrllibDownloader(BasicSourceLoader):
    def get_as_text(self, url):
        req = urllib.request.Request(url, headers={'User-agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        text = response.read().decode('utf-8')
        return text
