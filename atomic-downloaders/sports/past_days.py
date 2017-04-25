
import os
import os.path
import bs4
import json
import datetime
from data_module.data_lib.file_storage import prepare_dir
from data_module.data_lib.parsing_framework.namers.basic_namer import BasicNamer
from data_module.data_lib.parsing_framework.base_parser import BaseParser
from lib.args import date_parser_args
import simplejson
import re


class PastFootballDaysParser(BaseParser):
    # возвращает идентификатор сущности которую парсим
    def root_keys(self):
        return date_parser_args.date_range.get_days_from_end()

    def parse(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        match_links = soup.select('td.score-td a.score')

        entity = {
            'games_count': len(match_links),
            'matches': []
        }
        for link in match_links:

            tr = link.parent.parent
            start_time_tag = tr.select('td.alLeft')[0]
            owner_tag = tr.select_one('td.owner-td div.rel a.player')
            guest_tag = tr.select_one('td.guests-td div.rel a.player')
            owners_goals_tag = link.select_one('b span.s-left')
            guests_goals_tag = link.select_one('b span.s-right')
            status_match_tag = tr.select('td.alLeft')[-1]
            def get_id(link):
                url = link['href']
                identificator = re.findall(r'(\d+).html', url)

                # тут нужно еще что-то, ведь есть url по типу https://www.sports.ru/upl/dynamo-kiev-shakhtar/21-04-2017/
                if(len(identificator) <= 0):
                    return None
                return identificator[0]
            match = {
                "id": get_id(link), 
                'url': link['href'],
                'matchBegining': start_time_tag.text,
                'ownerGoal': owners_goals_tag.text  if guests_goals_tag is not None else None,
                'guestGoal': guests_goals_tag.text if guests_goals_tag is not None else None,
                'owner': owner_tag.text if owner_tag is not None else None,
                'visitor': guest_tag.text if guest_tag is not None else None,
            }
            entity['matches'].append(match)
        return entity


    def finalize(self, key, entity):
        respath = 'sports_date_%s.json' % (key.strftime('%Y-%m-%d'))
        print(respath)
        with open(respath, 'w') as f:
            json_text = simplejson.dumps(entity, ignore_nan=True)
            f.write(json_text)

namer = BasicNamer(
    get_filename=lambda key: 'sports_date_%s.html' % (key.strftime('%Y-%m-%d')),
    get_url=lambda key: 'https://www.sports.ru/stat/football/center/all/%s/%s/%s.html' % (key.strftime('%Y'), key.strftime('%m'), key.strftime('%d')) 
)
parser = PastFootballDaysParser(namer=namer)
parser.start()
