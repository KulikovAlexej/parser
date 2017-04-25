
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
        paragraph_count = len(soup.select('.game-info p'));
        def check_p(p_numb):
            if(paragraph_count > p_numb):
                return soup.select('.game-info p')[p_numb]
            else:
                return None
        def check_text(tag):
            if(tag != None and tag.text != None): 
                return tag.text
            else:
                return None
        def fill_goals(GoalTag):
            return {
            "goleador": GoalTag.text if GoalTag is not None else None,
            "goal_time": GoalTag.select_one('b').text
            }
        print(paragraph_count)
        score_tag = soup.select_one('.score.js-match-score')
        owner_tag = soup.select_one('.command.floatL .about-command .titleH2')
        visitor_tag = soup.select_one('.command.floatR .about-command .titleH2')
        league_tag = soup.select('.game-info p a')[0]
        date_tag = soup.select('.game-info p')[1]
        stadium_tag = soup.select('.game-info p')[2]
        status_tag = soup.select_one('.game-info .mB20.js-match-status')
        judje_tag = check_p(3)
        judgeAssistant_tag = check_p(4)
        spareJudge = check_p(5)
        ownerGoals_tag = soup.select('.js-first-team p')
        visitorGoals_tag = soup.select('.js-second-team p')
          
        entity = {
            'score': check_text(score_tag),
            'owner': check_text(owner_tag),
            'visitor': check_text(visitor_tag),
            'league': check_text(league_tag), #кое-где пишет иномер тура
            'status': check_text(league_tag),
            'judje': check_text(judje_tag),
            'judgeAssistant': check_text(judgeAssistant_tag),
            'stadium': check_text(stadium_tag),
            'date': check_text(date_tag),
            # 'time': '18:30',
            'ownerGoals': list(map(fill_goals, ownerGoals_tag)),
            'visitorGoals': list(map(fill_goals, visitorGoals_tag))
        }
        print(entity['ownerGoals'][0]['goleador'])
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