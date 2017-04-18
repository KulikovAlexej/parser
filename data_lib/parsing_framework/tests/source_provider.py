import random
import unittest
from data_module.data_lib.match_info_key import MatchInfoKey
from ..source_providers.basic_source_provider import BasicSourceProvider
from ..namers.basic_namer import BasicNamer


class TestSourceProvider(unittest.TestCase):
    def setUp(self):
        self.basic_source_provider = BasicSourceProvider()

    def test_get_page(self):
        namer = BasicNamer(
            get_filename=lambda key: 'ttt',
            get_url=lambda key: 'http://ya.ru/'
        )
        key = MatchInfoKey('football', 'test_provider', 'test_page')
        text = self.basic_source_provider.get_page(key, namer)
        # print(text.encode('ascii', 'ignore'))  # utf-8 prints in windows console with errors


if __name__ == '__main__':
    unittest.main()
