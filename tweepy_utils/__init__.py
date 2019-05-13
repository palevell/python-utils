# tweepy_utils/__init__.py - Sunday, April 28, 2019

from os.path import abspath, basename, dirname, exists, join, getmtime, lexists, realpath, splitext

__MODULE__ = splitext(basename(__file__))[0]

# Twitter API Function Wrappers
def get_blocked_ids():
	_proc_sig = __MODULE__ + '.get_blocked_ids()'
	ids = []
	tacct = me.screen_name
	filename = join(acct_cache, "%s_blocked_ids_%s.txt.bz2" % (tacct, fdate))
	# linkname = filename.replace(fdate, 'latest')
	if exists(filename):
		ids = load_ids(filename)
		""" if getmtime(filename) > id_refresh_ts:
			with bz2.open(filename, 'rt') as f:
				for line in f.readlines():
					try:
						ids.append(int(line))
					except Exception as e:
						print(_proc_sig, line, "Exception:", filename, e, file=sys.stderr, flush=True)
						continue"""
	if not ids:
		ids = api.blocks_ids()
		save_ids(filename, ids)
	# make_symlink(filename, linkname, overwrite=True)
	return ids

def add_list_members(list_info, user_ids=None, user_names=None):
	_proc_sig = __MODULE__ + '.add_list_members()'
	dlog.enter(_proc_sig)
	if user_ids is None and user_names is None:
		return
	result = None
	list_id = list_info.id
	mode = list_info.mode
	batch_len = 100
	batches = (user_ids[i:i+batch_len] for i in range(0, len(user_ids), batch_len))
	for batch_count, batch in enumerate(batches):
		result = None
		if DEBUG:
			dlog.print("api.add_list_members()", _proc_sig)
		if not DRYRUN:
			sleep(uniform(0.1, 0.6))
			retries = 3
			while retries > 0:
				retries -= 1
				try:
					result = api.add_list_members(list_id=list_id, user_id=batch)
					retries = -1
					debug_breakpoint()
				except tweepy.TweepError as e:
					if retries > 0:
						sleep(uniform(30,90))
					else:
						dlog.eprint("TweepError:", e.api_code, e.reason, batch, result, _proc_sig)
				except Exception as e:
					if retries > 0:
						sleep(uniform(30,90))
					else:
						dlog.eprint("Exception:", e, batch, result, _proc_sig)
	dlog.exit(_proc_sig)
	return

def extract_ids(list_of_objects):
	_proc_sig = __MODULE__ + '.extract_ids()'

	dlog.enter(_proc_sig)
	ids = []
	try:
		for item in list_of_objects:
			ids.append(item.id)
	except Exception as e:
		dlog.eprint("Exception: %s" % e, _proc_sig)
	dlog.exit(_proc_sig)
	return ids

def get_friends_ids(id=None, screen_name=None):
	_proc_sig = __MODULE__ + '.get_friends_ids()'

	dlog.enter(_proc_sig)
	# if user_id is provided, get screen_name
	if id is None and screen_name is None:
		tacct = me.screen_name
	elif id is not None:
		tacct = api.get_user(id).screen_name
	else:
		tacct = screen_name
	# Authorized accounts are stored in a separate folder
	if tacct in apis.keys():
		filename = join(acct_cache, "%s_friends_ids_%s.txt.bz2" % (tacct, fdate))
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	else:
		filename = join(user_cache, "%s_friends_ids_%s.txt.bz2" % (tacct, fdate))
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	# Get IDs
	ids = []
	if exists(filename):
		if getmtime(filename) > id_refresh_ts:
			# print('Loading IDs from %s' % filename, flush=True)
			with bz2.open(filename, 'rt') as f:
				for line in f.readlines():
					try:
						ids.append(int(line))
					except Exception as e:
						dlog.eprint("Exception: %s" % e, _proc_sig)
						continue
	if not ids:
		for page in tweepy.Cursor(api.friends_ids, screen_name=tacct).pages():
			ids.extend(page)
			sleep(uniform(3.05,6.06))
		save_ids(filename, ids)
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	dlog.exit(_proc_sig)
	return ids

def get_followers_ids(id=None, screen_name=None):
	_proc_sig = __MODULE__ + '.get_followers_ids()'

	dlog.enter(_proc_sig)
	# if user_id is provided, get screen_name
	if id is None and screen_name is None:
		tacct = me.screen_name
	elif id is not None:
		tacct = api.get_user(id).screen_name
	else:
		tacct = screen_name
	# Authorized accounts are stored in a separate folder
	if tacct in apis.keys():
		filename = join(acct_cache, "%s_followers_ids_%s.txt.bz2" % (tacct, fdate))
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	else:
		filename = join(user_cache, "%s_followers_ids_%s.txt.bz2" % (tacct, fdate))
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	# Get IDs
	ids = []
	if exists(filename):
		if getmtime(filename) > id_refresh_ts:
			with bz2.open(filename, 'rt') as f:
				for line in f.readlines():
					try:
						ids.append(int(line))
					except Exception as e:
						dlog.eprint("Exception: %s" % e, _proc_sig)
						continue
	if not ids:
		for page in tweepy.Cursor(api.followers_ids, screen_name=tacct).pages():
			ids.extend(page)
			sleep(uniform(3.05,6.06))
		save_ids(filename, ids)
	# linkname = filename.replace(fdate, 'latest')
	# make_symlink(filename, linkname)
	dlog.exit(_proc_sig)
	return ids

def get_list_members(owner, slug):
	""" Owner & Slug are used in the filename
	:param owner: list ownwer
	:param slug:  list slug
	:return: list of Twitter IDs
	"""
	_proc_sig = __MODULE__ + '.get_list_members()'

	dlog.enter(_proc_sig)
	user_filename = join(acct_cache, "%s_%s_users_%s.yaml.bz2" % (owner, slug, fdate))
	# user_linkname = user_filename.replace(fdate, 'latest')
	id_filename = join(acct_cache, "%s_%s_ids_%s.txt.bz2" % (owner, slug, fdate))
	# id_linkname = id_filename.replace(fdate, 'latest')
	users = []
	if exists(user_filename):
		if getmtime(user_filename) > id_refresh_ts:
			users = load_yaml(user_filename)
	if not users:
		# Since some lists are private, we'll use the API for the list owner
		if owner != me.screen_name and owner in apis:
			api2 = apis[owner]
		else:
			api2 = api
		list_id = api2.get_list(owner_screen_name=owner, slug=slug).id
		for page in tweepy.Cursor(api2.list_members, list_id=list_id).pages():
			users.extend(page)
			sleep(uniform(3.05,6.06))
		save_yaml(user_filename, users)
	# make_symlink(user_filename, user_linkname)
	# Extract user IDs and save
	if not exists(id_filename):
		ids = []
		for u in users:
			ids.append(u.id)
		save_ids(id_filename, ids)
	# make_symlink(id_filename, id_linkname)
	dlog.exit(_proc_sig)
	return users

def get_list_member_ids(owner, slug):
	_proc_sig = __MODULE__ + '.get_list_member_ids()'

	dlog.enter(_proc_sig)
	ids = []
	filename = join(acct_cache, "%s_%s_ids_%s.txt.bz2" % (owner, slug, fdate))
	if exists(filename):
		ids = load_ids(filename)
	if not ids:
		users = get_list_members(owner, slug)
		ids = extract_ids(users)
	dlog.exit(_proc_sig)
	return ids

def get_user_objects(user_ids, json_only=True):
	_proc_sig = __MODULE__ + '.whoarethey()'
	batch_len = 100
	batches = (user_ids[i:i+batch_len] for i in range(0, len(user_ids), batch_len))
	all_data = []
	for batch_count, batch in enumerate(batches):
		sleep(uniform(0.1, 0.6))
		users_list = api.lookup_users(user_ids=batch, tweet_mode='extended')
		if json_only:
			users_json = ([t._json for t in users_list])
			all_data += users_json
		else:
			all_data += users_list
	return all_data

def remove_list_members(list_info, user_ids=None, user_names=None):
	_proc_sig = __MODULE__ + '.remove_list_members()'
	dlog.enter(_proc_sig)
	if user_ids is None and user_names is None:
		return
	result = None
	list_id = list_info.id
	mode = list_info.mode
	batch_len = 100
	batches = (user_ids[i:i+batch_len] for i in range(0, len(user_ids), batch_len))
	for batch_count, batch in enumerate(batches):
		result = None
		if DEBUG:
			dlog.print("api.remove_list_members()", _proc_sig)
		if not DRYRUN:
			sleep(uniform(0.1, 0.6))
			retries = 3
			while retries > 0:
				retries -= 1
				try:
					result = api.remove_list_members(list_id=list_id, user_id=batch)
					retries = -1
					debug_breakpoint()
				except tweepy.TweepError as e:
					if retries > 0:
						sleep(uniform(30,90))
					else:
						dlog.eprint("TweepError:", e.api_code, e.reason, batch, result, _proc_sig)
				except Exception as e:
					if retries > 0:
						sleep(uniform(30,90))
					else:
						dlog.eprint("Exception:", e, batch, result, _proc_sig)
	dlog.exit(_proc_sig)
	return
