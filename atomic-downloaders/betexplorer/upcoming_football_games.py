
import os
import os.path
import bs4
import datetime
from lib.mongo_connector import connector
from data_module.data_lib.file_storage import prepare_dir
from data_module.data_lib.parsing_framework.namers.basic_namer import BasicNamer
from data_module.data_lib.parsing_framework.base_parser import BaseParser
from lib.args import date_parser_args


class UpcomingFootballGamesParser(BaseParser):
    def root_keys(self):
        for n in [n+date_parser_args.date_shift for n in range(date_parser_args.date_limit)]:
            date = date_parser_args.today - datetime.timedelta(days=n+1)
            print(date)
            day_entity = connector.football_betexp_upcoming_days.find_one({'key': date})
            for match in day_entity['matches']:
                match['betexp_id'] = match['url'].split('/')[-2]
                dt_split = match['datetime'].split(',')
                year = int(dt_split[2])
                month = int(dt_split[1])
                day = int(dt_split[0])
                match['date'] = datetime.datetime(year, month, day, int(dt_split[3]), int(dt_split[4]))
                if year == date.year and month == date.month and day == date.day:
                    yield match

    def parse(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        breadcrumbs = soup.select('.list-breadcrumb li')
        country_tag = breadcrumbs[2].select_one('a')
        competition_tag = breadcrumbs[3].select_one('a')
        team_1_tag = soup.select('.list-details__item__title a')[0]
        team_2_tag = soup.select('.list-details__item__title a')[1]
        datetime_tag = soup.select_one('#match-date')

        entity = {
            'country': country_tag.text,
            'competition': competition_tag.text,
            'team_1_name': team_1_tag.text,
            'team_2_name': team_2_tag.text,
            'team_1_url': team_1_tag['href'],
            'team_2_url': team_2_tag['href'],
            'datetime': datetime_tag['data-dt'],
        }
        return entity

    def finalize(self, key, entity):
        entity['key'] = key['betexp_id']
        entity['source_url'] = self.namer.get_url(key)
        entity['created_at'] = datetime.datetime.utcnow()
        connector.football_betexp_upcoming_games.update({'key': entity['key']}, entity, upsert=True)

namer = BasicNamer(
    get_filename=lambda key: os.path.join(prepare_dir('betexplorer', key['date'], 'upcoming_game'), '%s_d%s.html' % (key['betexp_id'], date_parser_args.upcoming)),
    get_url=lambda key: 'http://www.betexplorer.com%s' % key['url']
)
parser = UpcomingFootballGamesParser(namer=namer)
parser.start()
