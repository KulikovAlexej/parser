
import os
import os.path
import bs4
import json
import datetime
from lib.mongo_connector import connector
from data_module.data_lib.file_storage import prepare_dir
from data_module.data_lib.parsing_framework.namers.basic_namer import BasicNamer
from data_module.data_lib.parsing_framework.base_parser import BaseParser
from lib.args import date_parser_args


class PastFootballDaysParser(BaseParser):
    def root_keys(self):
        for n in [n+date_parser_args.date_shift for n in range(date_parser_args.date_limit)]:
            date = date_parser_args.today - datetime.timedelta(days=n+1)
            print(date)
            key_found_count = connector.football_betexp_days.count({'key': date})
            if key_found_count == 0:
                yield date

    def parse(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        match_links = soup.select('td.table-matches__tt a')
        entity = {
            'games_count': len(match_links),
            'matches': []
        }
        for link in match_links:
            tr = link.parent.parent
            start_time_tag = tr.select_one('span.table-matches__time')
            score_ft_tag = tr.select_one('td.table-matches__result')
            score_ht_tag = tr.select_one('td.table-matches__partial')
            competition_tag = tr.parent.select_one('tr.js-tournament a.table-matches__tournament')

            match = {
                'url': link['href'],
                'datetime': tr['data-dt'],
                'visible': tr['data-def'],
                'start_time': start_time_tag.text if start_time_tag is not None else None,
                'teams_name_cut': link.text,
                'score_ft': score_ft_tag.text if score_ft_tag is not None else None,
                'score_ht': score_ht_tag.text if score_ht_tag is not None else None,
                'competition': competition_tag.text if competition_tag is not None else None,
            }
            entity['matches'].append(match)
        return entity

    def finalize(self, key, entity):
        entity['key'] = key
        entity['source_url'] = self.namer.get_url(key)
        entity['created_at'] = datetime.datetime.utcnow()
        try:
            connector.football_betexp_days.insert(entity)
        except connector.DuplicateKeyError:
            pass

namer = BasicNamer(
    get_filename=lambda key: os.path.join(prepare_dir('betexplorer', key, 'past_day'), 'day.html'),
    get_url=lambda key: 'http://www.betexplorer.com/results/soccer/?year=%i&month=%i&day=%i' % (key.year, key.month, key.day)
)
parser = PastFootballDaysParser(namer=namer)
parser.start()
