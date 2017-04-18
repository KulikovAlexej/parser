
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


class PastFootballGamesParser(BaseParser):
    def root_keys(self):
        for n in [n+date_parser_args.date_shift for n in range(date_parser_args.date_limit)]:
            date = date_parser_args.today - datetime.timedelta(days=n+1)
            print(date)
            day_entity = connector.football_betexp_days.find_one({'key': date})
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
        score_ft_tag = soup.select_one('#js-score')
        score_ht_tag = soup.select_one('#js-partial')
        score_note_tag = soup.select_one('#js-eventstage')
        goals_sections = soup.select('.list-details--shooters .list-details__item')

        def _extract_goals_fl(row):
            return {
                'note': row.select('td')[0].text,
                'minute': row.select('td')[1].text,
                'player': row.select('td')[2].text,
            }

        def _extract_goals_fr(row):
            return {
                'note': row.select('td')[2].text,
                'minute': row.select('td')[0].text,
                'player': row.select('td')[1].text,
            }

        goals_team_1 = list(map(_extract_goals_fl, goals_sections[0].select('tr'))) if len(goals_sections) == 2 else None
        goals_team_2 = list(map(_extract_goals_fr, goals_sections[1].select('tr'))) if len(goals_sections) == 2 else None
        entity = {
            'country': country_tag.text,
            'competition': competition_tag.text,
            'team_1_name': team_1_tag.text,
            'team_2_name': team_2_tag.text,
            'team_1_url': team_1_tag['href'],
            'team_2_url': team_2_tag['href'],
            'datetime': datetime_tag['data-dt'],
            'score_ft': score_ft_tag.text if score_ft_tag is not None else None,
            'score_ht': score_ht_tag.text if score_ht_tag is not None else None,
            'score_note': score_note_tag.text if score_note_tag is not None else None,
            'goals_1': goals_team_1,
            'goals_2': goals_team_2,
        }
        return entity

    def finalize(self, key, entity):
        entity['key'] = key['betexp_id']
        entity['source_url'] = self.namer.get_url(key)
        entity['created_at'] = datetime.datetime.utcnow()
        try:
            connector.football_betexp_games.insert(entity)
        except connector.DuplicateKeyError:
            pass

namer = BasicNamer(
    get_filename=lambda key: os.path.join(prepare_dir('betexplorer', key['date'], 'past_game'), '%s.html' % key['betexp_id']),
    get_url=lambda key: 'http://www.betexplorer.com%s' % key['url']
)
parser = PastFootballGamesParser(namer=namer)
parser.start()
