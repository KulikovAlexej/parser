
import os.path
import datetime
from configs.platform import export_path


def get_dir_name_v1(vendor, date, page_type='common'):
    year = datetime.datetime.strftime(date, '%Y')
    month = datetime.datetime.strftime(date, '%m')
    day = datetime.datetime.strftime(date, '%d')
    return os.path.join(export_path, vendor, page_type, year, month, day)
