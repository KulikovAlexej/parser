
import os
import bs4
import json
import datetime
from lib.mongo_connector import connector
from data_module.data_lib.file_storage import prepare_dir
from lib.args import date_parser_args


def get_match_items():
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


def extract_odds(row):
        if row is None:
            return None
        else:
            try:
                tds = row.find_all('td')
                if len(tds) == 6:
                    return {
                        'bookmaker': tds[0].string,
                        'win_1': tds[3].get('data-odd'),
                        'win_x': tds[4].get('data-odd'),
                        'win_2': tds[5].get('data-odd'),
                        'win_1_date': tds[3].get('data-created'),
                        'win_x_date': tds[4].get('data-created'),
                        'win_2_date': tds[5].get('data-created'),
                    }
                elif len(tds) == 5 or len(tds) == 0:
                    return None
                else:
                    raise Exception('Unexpected number of td')
            except Exception as e:
                return {
                    'error': True,
                    'error_text': str(e),
                    'row': str(row),
                }


match_items = get_match_items()
for item in match_items:
    match_id = item['betexp_id']
    source_url = 'http://www.betexplorer.com%s' % item['url']
    match_date = item['date']

    output_dir = prepare_dir('betexplorer', match_date, 'upcoming_odds_win')
    filename = '%s/id_%s_d%s.html' % (output_dir, match_id, date_parser_args.upcoming)

    if not os.path.isfile(filename) or os.path.getsize(filename) < 2000:
        cmd = "curl 'http://www.betexplorer.com/gres/ajax/matchodds.php?p=1&e=" + match_id + "&b=1x2' -H 'Cookie: new_version=1; my_timezone=%2B1; infobox-new_promo=1; _gat_UA-191939-1=1; js_cookie=1; widget_timeStamp=1484878529; my_cookie_id=63568996; my_cookie_hash=448bc8d270143e796ccefc656626874d; widget_pageViewCount=2; _ga=GA1.2.1301231815.1477358241' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,ru;q=0.6,und;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: " + source_url + "' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed > " + filename
        os.system(cmd)

    print('read %s' % filename)
    try:
        file = open(filename, encoding='utf-8', mode='r')
        content = file.read()
        file.close()
        jsonresponse = json.loads(str(content))
        html = jsonresponse['odds']

        soup = bs4.BeautifulSoup(html, 'html')
        trs = soup.select('table tr')
        odds_win = list(filter(lambda o: o is not None, map(extract_odds, trs)))

        entity = {
                'key': match_id,
                'source_url': source_url,
                'odds_win': odds_win,
                'created_at': datetime.datetime.utcnow()
        }
        connector.football_betexp_upcoming_odds_win.update({'key': match_id}, entity, upsert=True)
    except Exception as e:
        print(item)
        raise e
