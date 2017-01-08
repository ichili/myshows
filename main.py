import sys
import ntpath
from datetime import datetime
from myshows.api_client import MyShowsClient
from myshows.exceptions import *
from notifu import notify
import json

log_path = 'log.txt'

def log(log_string):
	path = ntpath.dirname(sys.argv[0])
	log_string = str(log_string)
	with open(ntpath.join(path, log_path), 'a') as f:
		f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : ')
		f.write(log_string + '\n')

def read_setting():
	path = ntpath.dirname(sys.argv[0])
	with open(ntpath.join(path, 'settings.txt'), 'r') as f:
		settings = f.readlines()
	credentials = {}
	for s in settings:
		x, y = s.split('=')
		x = x.strip()
		y = y.strip()
		credentials[x] = y
	return credentials
	

def main():
	log("main")
	try:
		log("read")
		credentials = read_setting()
		client = MyShowsClient(credentials['login'], credentials['password']) 
		log("try_login")
		client.login()
		log("success")
		notify_str = []
		for x in sys.argv[1:]:
			fname = ntpath.basename(x)
			sid = client.get_show_id(fname)
			print(client.checked_episodes(sid).keys())
			
			episode = client.find_episode(fname)
			if episode:
				client.check_episode(episode)
				showid = client.test(episode)['showId']
				#print(showid)
				#print (json.dumps(client.full_show_info(showid), indent=4, sort_keys=True))
				#print(client.full_show_info(showid))
				notify_str.append('Episode {} checked\n'.format(fname))
			else:
				notify_str.append('Can\'t find episode {}\n'.format(fname))
		notify(''.join(notify_str))
	except AuthorizationError as e:
		log(e)
		notify(e)


if __name__ == '__main__':
	main()
	input()