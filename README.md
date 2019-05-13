REAMDME

### Description
These utilities have evolved as I have been banging-out Python code for the last two years.
The functions that I was re-using the most are included in this repository.
Most of these came from working with Tweepy.

### Contents
- datetime_utils - UTC converters & daystart / midnight converter
	- local_to_utc(dt, naive=True)
	- midnight(dt)
	- utc_to_local(utc_dt)
- debug_utils - Debugging utilities ported from 20 years of coding in Visual Basic, SQL, etc.
	- enter(self, proc_sig, memo=None)
	- exit(self, memo=None)
	- current_proc(self)
	- print(self, *args, **kwargs)
	- eprint(self, *args, **kwargs)
- file_utils - Wrappers for saving CSV and YAML with optional BZip2 compression, plus touch() utility
	- save_csv(filename, rows, headers=None)
	- load_yaml(filename)
	- save_yaml(filename, data, batch_size=1000)
	- save_yaml_old(filename, data)
	- save_bad_tweet(tweet)
	- save_updated_tweet(tweet)
	- load_ids(filename)
	- save_ids(filename, ids)
	- touch(path, mode=0o644, create=True, utimes=None)
- tweepy_utils - Wrappers for Tweepy functions that employ "caching" to reduce API calls
	- get_blocked_ids()
	- add_list_members(list_info, user_ids=None, user_names=None)
	- extract_ids(list_of_objects)
	- get_friends_ids(id=None, screen_name=None)
	- get_followers_ids(id=None, screen_name=None)
	- get_list_members(owner, slug)
	- get_list_member_ids(owner, slug)
	- get_user_objects(user_ids, json_only=True)
	- remove_list_members(list_info, user_ids=None, user_names=None)

### Usage
1) Copy `util` folder(s) to your project folder
2) Add the appropriate `import` to your code, for example:
```python
import datetime_utils
import debug_utils
import file_utils
import tweepy_utils
```
