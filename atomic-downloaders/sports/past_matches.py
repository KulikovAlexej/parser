
import os
import os.path
import bs4
import json
import datetime
# from lib.mongo_connector import connector
from data_module.data_lib.file_storage import prepare_dir
from data_module.data_lib.parsing_framework.namers.basic_namer import BasicNamer
from data_module.data_lib.parsing_framework.base_parser import BaseParser
from lib.args import date_parser_args
import simplejson
import time


class PastFootballDaysParser(BaseParser):
    def root_keys(self):
        # на каждый день выбираем файл - прописываем путь
        # date_parser_args.date_range.get_days_from_end() - генератор со страницами, которые разбиты по датам
        print(date_parser_args.date_range.get_days_from_end())
        for date in date_parser_args.date_range.get_days_from_end():
            # datestr = datetime.strftime(date, "%Y-%m-%d")
            # print(date)

            respath = 'sports_date_%s.json' % (datetime.datetime.strftime(date, '%Y-%m-%d'))
            file = open(respath)
            file = file.read()
            # print(respath)
            # print(file)
            obj = simplejson.loads(file)
            # print(obj)
            for match in obj['matches']:
                if match['id'] is None or match['id'] == 'None':
                    continue
                yield (match['url'], match['id'])
                

                # for url in matches:
                #     yield obj['matches']
            # print(obj)
            # # for url in matches:
            # #     yield obj['matches']



    def parse(self, text):
        soup = bs4.BeautifulSoup(text, 'lxml')
        match_links = soup.select('td.score-td a.score')
        return {}

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
            
            match = {
                'url': link['href'],
                'matchBegining': start_time_tag.text,
                'ownerGoal': owners_goals_tag.text,
                'guestGoal': guests_goals_tag.text if guests_goals_tag is not None else None,
                'owner': owner_tag.text if owner_tag is not None else None,
                'visitor': guest_tag.text if guest_tag is not None else None,
            }
            entity['matches'].append(match)
        return entity
        

    def finalize(self, key, entity):
        # respath = 'sports_date_%s.json' % (key.strftime('%Y-%m-%d'))
        # print(respath)
        # with open(respath, 'w') as f:
        #     json_text = simplejson.dumps(entity, ignore_nan=True)
        #     f.write(json_text)
        pass

namer = BasicNamer(
    get_filename=lambda key: 'match_%s.html' % key[1],
    # get_url=lambda key: 'https://www.sports.ru/stat/football/center/all/%s/%s/%s.html' % (key.strftime('%Y'), key.strftime('%m'), key.strftime('%d')) 
    # simplejson(get_filename());
    get_url=lambda key: key[0]
)
parser = PastFootballDaysParser(namer=namer)
parser.start()
print('hello')