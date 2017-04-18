
import datetime


class MatchInfoKey(tuple):
    sport = None
    provider = None
    page_type = None
    date = None

    def __new__(cls, sport, provider, page_type, date=datetime.datetime.utcnow()):
        obj = super(MatchInfoKey, cls).__new__(cls, (sport, provider, page_type, date.year, date.month, date.day))
        return obj

    def __init__(self, sport, provider, page_type, date=datetime.datetime.utcnow()):
        self.sport = sport
        self.provider = provider
        self.page_type = page_type
        self.date = date
