import pytz
import logging
import datetime


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def converter(self, timestamp):
        # Create datetime in UTC
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        # Change datetime's timezone
        return dt.astimezone(pytz.timezone('Asia/Seoul'))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s


console = logging.FileHandler('UpdateSubsStatus.log')
console.setFormatter(Formatter(
        '%(asctime)s;%(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
logging.getLogger('').addHandler(console)
logging.warning("Critical event")

with open('UpdateSubsStatus.log', "rt", encoding="utf-8") as f:
    print(f.read())
