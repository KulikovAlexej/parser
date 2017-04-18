
import os.path
import urllib
import urllib.request
import datetime
from pandas import read_csv
import threading
import argparse

print('############################################')
print('### Nowgoal yesterday matches downloader ###')
print('############################################')

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=int, default=1)
args = parser.parse_args()
days_shift = args.d if args.d else 1

MAX_THREADS = 3
date = datetime.datetime.today() - datetime.timedelta(days=days_shift)
date_str = date.strftime('%Y-%m-%d')
print('date = %s' % date_str)
filename = 'tmp/nowgoal_listing_for_date/%s.csv' % date_str

matches = read_csv(filename, error_bad_lines=True, delimiter=";")
print('Found %i matches' % len(matches))


def handle_page(page_url, file_path):
    if not os.path.isfile(file_path):
        urllib.request.urlretrieve(page_url, file_path)


def create_dir_if_not_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def init_subfolder_for_given_date(date_str):
    create_dir_if_not_exists('tmp/nowgoal_past_matches')
    create_dir_if_not_exists('tmp/nowgoal_past_matches/' + date_str)
    create_dir_if_not_exists('tmp/nowgoal_past_matches/' + date_str + '/analysis')
    create_dir_if_not_exists('tmp/nowgoal_past_matches/' + date_str + '/detail')
    create_dir_if_not_exists('tmp/nowgoal_past_matches/' + date_str + '/3in1odds-ft')
    create_dir_if_not_exists('tmp/nowgoal_past_matches/' + date_str + '/3in1odds-ht')


init_subfolder_for_given_date(date_str)

print('Downloading started')
for n in matches.index:
    try:
        mid = str(matches.id[n])
        # handle_page('http://data.nowgoal.com/analysis/' + mid + '.html', 'tmp/nowgoal_past_matches/' + date_str + '/analysis/' + mid + '.html')
        handle_page('http://data.nowgoal.com/detail/' + mid + '.html', 'tmp/nowgoal_past_matches/' + date_str + '/detail/' + mid + '.html')
        handle_page('http://data.nowgoal.com/3in1odds/3_' + mid + '.html', 'tmp/nowgoal_past_matches/' + date_str + '/3in1odds-ft/' + mid + '.html')
        handle_page('http://data.nowgoal.com/3in1odds/3_' + mid + '_2.html', 'tmp/nowgoal_past_matches/' + date_str + '/3in1odds-ht/' + mid + '.html')
        print('downloaded ' + str(n + 1) + ' of ' + str(len(matches.index)))
    except Exception as e:
        print('error downloading ' + str(n))
        print(e)

print('Downloading complete!')
