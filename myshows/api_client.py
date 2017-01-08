from . import api
from .exceptions import *
from guessit import guessit

class MyShowsClient:
	
	def __init__(self, login, password):
		self._login = login
		self._password = password
		self.api = api.Session()

	def login(self):
		return self.api.login(self._login, self._password)

	def check_episode(self, id, rating=None):
		return self.api.check_episode(id, rating=rating)

	def uncheck_episode(self, id, rating=None):
		return self.api.uncheck_episode(id, rating=rating)
	
	def find_episode(self, filename):
		try:
			episode = self.search_filename(filename)
		except:
			try:
				info = self.guess(filename)
				show_title = info['title']
				show = self.api.search(show_title)
				print(show)
				show_id = int(list(show.keys())[0])
				show_info = self.api.full_show_info(show_id)
				for k, v in show_info['episodes'].items():
					if v['seasonNumber'] == info['season'] and v['episodeNumber'] == info['episode']:
						episode = v['id']
						break
				else:
					return None
			except:
				return None
		return episode


	def search_filename(self, filename):
		info = self.api.search_filename(filename)
		episode = list(info['show']['episodes'].keys())[0]
		return episode

	def search(self, name):
		return self.api.search(name)

	def test(self, show_id):
		show_info = self.api.episode_info(show_id)
		return show_info	

	def full_show_info(self, show_id):
		show_info = self.api.full_show_info(show_id)
		return show_info	
	
	@staticmethod
	def guess(filename):
		return dict(guessit(filename))