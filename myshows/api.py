import requests
from .exceptions import *
from .constants import *
from hashlib import md5

class Session:

	def __init__(self):
		self.session = requests.Session()

	def __request(self, url, params=None, json=True):
		try:
			response = self.session.post(url, params=params)
		except:
			raise
		status = response.status_code
		if status != 200:
			if status == 401:
				raise AuthorizationRequiredError()
			elif status == 403:
				raise AuthorizationError()
			elif status == 404:
				raise WrongParametersError()
			elif status == 500:
				raise MissingParameterError()
			else:
				raise UnknownError()
		if json:
			return response.json()
		return response
	
	def __md5(self, string):
		return md5(string.encode('utf-8')).hexdigest()
	
	def login(self, login, password):
		url = API_HOST + LOGIN
		credentials = {'login': login, 'password': self.__md5(password)}
		self.__request(url, params=credentials, json=False)
		return True

	def profile(self):
		url = API_HOST + PROFILE
		return self.__request(url)

	def shows(self):
		url = API_HOST + USER_SHOWS
		return self.__request(url)

	def __set_episode_status(self, id, status, rating=None):
		params = {}

		if status == 'check':
			url = API_HOST + CHECK_EPISODE + str(id).strip()
			if rating:
				params['rating'] = rating
		elif status == 'uncheck':
			url = API_HOST + UNCHECK_EPISODE + str(id).strip()
		self.__request(url, params=params, json=False)
		return True

	def check_episode(self, id, rating=None):
		return self.__set_episode_status(id, 'check', rating=rating)

	def uncheck_episode(self, id, rating=None):
		return self.__set_episode_status(id, 'uncheck', rating=rating)

	def sync_episodes(self, show_id, *episodes):
		pass

	def sync_episodes_delta(self, show_id, **episodes):
		pass

	def set_show_status(self, id, status):
		if status not in ['watching', 'later', 'cancelled', 'remove']:
			raise WrongParametersError()
		url = API_HOST + USER_SHOWS + str(id) + '/' + str(status)
		return self.__request(url)

	def rate_show(self, id, rating):
		if rating not in range(1, 6):
			raise WrongParametersError()
		url = API_HOST + USER_SHOWS + str(id) + '/rate/' + str(rating)
		return self.__request(url)

	def rate_episode(self, id, rating):
		if rating not in range(1, 6):
			raise WrongParametersError()
		#url = API_HOST + 
	def rate_episodes(self, **ratings):
		pass

	def search(self, query):
		url = API_HOST + SEARCH
		params = {'q': query}
		return self.__request(url, params=params)

	def search_filename(self, filename):
		url = API_HOST + SEARCH_FILENAME
		params = {'q': filename}
		return self.__request(url, params=params)

	def checked_episodes(self, show_id):
		url = API_HOST + USER_SHOWS + str(show_id) +'/'
		return self.__request(url)

	def episode_info(self, id):
		url = API_HOST + EPISODES + str(id)
		print(url)
		return self.__request(url)

