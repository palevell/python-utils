# file_utils/__init__.py - Saturday, April 27, 2019
""" File Utilities """
__version__ = '0.1.9'

from datetime import datetime
from debug_utils import DebugLog, Verbosity
from os.path import basename, exists, join, splitext
from pathlib import Path
from tempfile import mkstemp
from time import sleep
import oyaml as yaml
import builtins, bz2, csv, os, shutil

__MODULE__ = splitext(basename(__file__))[0]

_dlog = DebugLog(verbosity=Verbosity.Errors)

def save_csv(filename, rows, headers=None):
	_proc_sig = __MODULE__ + '.save_csv()'
	_dlog.enter(_proc_sig)
	tempfile = mkstemp('.csv', __MODULE__)[1]
	if headers is not None:
		rows = [ headers, ] + rows
	try:
		with open(tempfile, 'wt') as csvfile:
			csv.writer(csvfile).writerows(rows)
		try:
			os.renames(tempfile, filename)
		except IOError:
			try:
				shutil.move(tempfile, filename)
			except IOError as e:
				_dlog.eprint("Exception:", filename, e, _proc_sig)
				_dlog.exit(_proc_sig)
				raise
	except Exception as e:
		_dlog.eprint("Exception:", filename, e, _proc_sig)
		_dlog.exit(_proc_sig)
		raise
	_dlog.exit(_proc_sig)
	return

def load_yaml(filename):
	_proc_sig = __MODULE__ + '.load_yaml()'

	_dlog.enter(_proc_sig)
	data = None
	# We're getting fancy, here - supporting BZip2 compression
	if not filename.endswith('.bz2'):
		open = builtins.open
	else:
		open = bz2.open
	with open(filename, 'rt') as r:
		try:
			data = yaml.load(r, Loader=yaml.FullLoader)
		except yaml.MarkedYAMLError as e:
			_dlog.eprint("yaml.MarkedYAMLError:", e, _proc_sig, filename)
		except yaml.YAMLError as e:
			_dlog.eprint("yaml.YAMLError:", e, _proc_sig, filename)
		except Exception as e:
			_dlog.eprint("Exception:", e, _proc_sig, filename)
			_dlog.exit(_proc_sig)
	_dlog.exit(_proc_sig)
	return data

def save_yaml(filename, data, batch_size=1000):
	_proc_sig = __MODULE__ + '.save_yaml()'
	_dlog.enter(_proc_sig)

	if type(data) is not list:
		data = [ data, ]
	data_items = len(data)
	paginate = data_items > batch_size

	# We're getting fancy, here - supporting BZip2 compression
	if filename.endswith('.bz2'):
		open = bz2.open
	else:
		open = builtins.open
	try:
		batches = (data[i:i+batch_size] for i in range(0, len(data), batch_size))
		for batch_count, batch in enumerate(batches):
			if paginate:
				page_num = batch_count + 1
				pagename = filename.replace('.yaml', '_P%02d.yaml' % page_num)
				tmpfile = mkstemp(prefix=pagename+'.', dir='')[1]
				target = pagename
			else:
				tmpfile = mkstemp(prefix=filename+'.', dir='')[1]
				target = filename
			with open(tmpfile, 'wt') as w:
				yaml.dump(batch, w)
			shutil.move(tmpfile, target)
	except IOError as e:
		_dlog.eprint("IOError:", filename, e, _proc_sig)
		raise
	except Exception as e:
		_dlog.eprint("Exception:", filename, e, _proc_sig)
		raise
	_dlog.exit(_proc_sig)
	return

def save_yaml_old(filename, data):
	_proc_sig = __MODULE__ + '.save_yaml()'
	_dlog.enter(_proc_sig)

	if type(data) is not list:
		data = [ data, ]
	batch_size = 1000
	data_items = len(data)
	paginate = data_items > batch_size
	
	# We're getting fancy, here - supporting BZip2 compression
	if filename.endswith('.bz2'):
		open = bz2.open
	else:
		open = builtins.open
	try:
		for batch_offset in range(0, data_items, batch_size):
			batch_limit = batch_offset + batch_size - 1
			if batch_limit > data_items:
				batch_limit = data_items
			page_num = batch_offset / batch_size + 1
			if not paginate:
				tmpfile = join(_tmpdir, basename(filename))
				target = filename
			else:
				pagename = filename.replace('.yaml', '_P%02d.yaml' % page_num)
				tmpfile = join(_tmpdir, basename(pagename))
				target = pagename
			with open(tmpfile, 'wt') as w:
				yaml.dump(data[batch_offset:batch_limit], w)
			shutil.move(tmpfile, target)
	except IOError as e:
		_dlog.eprint("IOError:", filename, e, _proc_sig)
		raise
	except Exception as e:
		_dlog.eprint("Exception:", filename, e, _proc_sig)
		raise
	_dlog.exit(_proc_sig)
	return

def save_bad_tweet(tweet):
	dt = datetime.now().strftime("%Y%m%d_%H%M%S")
	fname = 'problem_tweet_%d_%s.yaml' % (tweet.id, dt)
	while exists(fname):
		sleep(1)
		fname = 'problem_tweet_%d_%s.yaml' % (tweet.id, dt)
	save_yaml(fname, tweet)
	return

def save_updated_tweet(tweet):
	dt = datetime.now().strftime("%Y%m%d_%H%M%S")
	fname = 'updated_tweet_%d_%s.yaml' % (tweet.id, dt)
	while exists(fname):
		sleep(1)
		fname = 'updated_tweet_%d_%s.yaml' % (tweet.id, dt)
	save_yaml(fname, tweet)
	return

def load_ids(filename):
	_proc_sig = __MODULE__ + '.load_ids()'

	_dlog.enter(_proc_sig)
	ids = []
	# We're getting fancy, here - supporting BZip2 compression
	if not filename.endswith('.bz2'):
		open = builtins.open
	else:
		open = bz2.open
	# print('Loading IDs from %s' % filename, flush=True)
	with open(filename, 'rt') as f:
		for line in f.readlines():
			try:
				ids.append(int(line))
			except Exception as e:
				_dlog.eprint(line, "Exception:", e, _proc_sig)
				continue
	# print('Loaded %d IDs from %s' % (len(ids), filename), flush=True)
	_dlog.exit(_proc_sig)
	return ids

def save_ids(filename, ids):
	_proc_sig = __MODULE__ + '.save_ids()'

	_dlog.enter(_proc_sig)
	lines = []
	for id in ids:
		line = str(id)
		if not line.endswith(os.linesep):
			line = line + os.linesep
		lines.append(line)
	# We're getting fancy, here - supporting BZip2 compression
	if not filename.endswith('.bz2'):
		open = builtins.open
	else:
		open = bz2.open
	with open(filename, 'wt') as f:
		f.writelines(lines)
	_dlog.exit(_proc_sig)
	return

def touch(path, mode=0o644, create=True, utimes=None):
	if not exists(path) and create is True:
		Path(path).touch(mode=0o644)
	if utimes:
		os.utime(path, utimes)
	return

if __name__ == '__main__':
	# This doesn't run when stuff is imported
	do_nothing = True
