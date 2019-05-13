# datetime_utils/__init__.py - Saturday, April 27, 2019
""" Date/Time Utilities """
__version__ = '0.0.1'

from datetime import datetime, timezone
from os.path import basename, exists, join, splitext
from time import sleep
from tzlocal import get_localzone

__MODULE__ = splitext(basename(__file__))[0]

# Date/Time Functions
def local_to_utc(dt, naive=True):
	if dt.tzinfo is None:
		raise ValueError("Missing time zone")
	if type(dt) is not datetime:
		raise TypeError("Expected datetime value")
	dt = dt.astimezone(timezone.utc)
	if naive:
		dt = dt.replace(tzinfo=None)
	return dt

def midnight(dt):
	if type(dt) is not datetime:
		raise TypeError("Expected datetime value")
	return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def utc_to_local(utc_dt):
	return utc_dt.replace(tzinfo=timezone.utc).astimezone(get_localzone())

if __name__ == '__main__':
    tz1 = get_localzone()
