import requests
from .exceptions import *
from .constants import *
from hashlib import md5

class Session:

	def __init__(self):
		self.session = requests.Session()

	def __request(self, url, params=None, json=True):
		url = API_HOST + url
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

	def __set_episode_status(self, id, status, rating=None):
		'''
			Sets the episode with given Id checked/unchecked
			rates episode if rating is provided
		'''
		params = {}

		if status == 'check':
			url = CHECK_EPISODE + str(id).strip()
			if rating:
				params['rating'] = rating
		elif status == 'uncheck':
			url = UNCHECK_EPISODE + str(id).strip()
		self.__request(url, params=params, json=False)
		return True
	
	#Авторизация
	def login(self, login, password):
		'''
			Takes login and password
			returns True if authentification is successfull
		'''
		url = LOGIN
		credentials = {'login': login, 'password': self.__md5(password)}
		self.__request(url, params=credentials, json=False)
		return True
	
	#Профиль пользователя
	def profile(self):
		'''
			Returns user profile
		'''
		url = PROFILE
		return self.__request(url)
	
	#Список сериалов
	def shows(self):
		'''
			Returns list of user's shows
		'''
		url = USER_SHOWS
		return self.__request(url)
	
	#Список просмотренных серий
	def checked_episodes(self, show_id):
		'''
			Returns information about all episodes of
			given show marked as seen
		'''
		url = USER_SHOWS + str(show_id) +'/'
		return self.__request(url)

	#TODO Список серий(прошлых, будущих, по сериалу)

	#Отмечание эпизода
	def check_episode(self, id, rating=None):
		'''
			Sets episode status as seen
			rates episode if rating provided
		'''
		return self.__set_episode_status(id, 'check', rating=rating)

	#Снятие флага об отмеченном эпизоде
	def uncheck_episode(self, id, rating=None):
		'''
			Sets episode status as unseen
			rates episode if rating provided			
		'''
		return self.__set_episode_status(id, 'uncheck', rating=rating)

	#Синхронизация всех просмотренных эпизодов (полная)
	def sync_episodes(self, show_id, *episodes):
		pass

	#Синхронизация всех просмотренных эпизодов (дельта)
	def sync_episodes_delta(self, show_id, **episodes):
		pass

	#Управление статусом сериала
	def set_show_status(self, id, status):
		'''
			Switches current watching status of given show
		'''
		if status not in ['watching', 'later', 'cancelled', 'remove']:
			raise WrongParametersError()
		url = USER_SHOWS + str(id) + '/' + str(status)
		return self.__request(url)

	#Управление рейтингом сериала
	def rate_show(self, id, rating):
		'''
			Sets rating for the show
		'''
		if rating not in range(1, 6):
			raise WrongParametersError()
		url = USER_SHOWS + str(id) + '/rate/' + str(rating)
		return self.__request(url)

	#Управление рейтингом эпизода
	def rate_episode(self, id, rating):
		'''
			Sets rating for the episode
		'''
		if rating not in range(1, 6):
			raise WrongParametersError()
		#url = 

	#Массовое управление рейтингом эпизодов
	def rate_episodes(self, **ratings):
		pass

	#TODO Новости друзей

	#TODO Комментарии

	#TODO Отметить как прочитанные

	#Поиск
	def search(self, query):
		'''
			Search show by it's name
		'''
		url = SEARCH
		params = {'q': query}
		return self.__request(url, params=params)

	#Поиск эпизодов по файлу
	def search_filename(self, filename):
		'''
			Search show/episode by filename of video
			provided by user
		'''
		url = SEARCH_FILENAME
		params = {'q': filename}
		return self.__request(url, params=params)

	#Информация о сериале со списком эпизодов
	def full_show_info(self, id):
		'''
			Returns detailed information about 
			the show
		'''
		url = SHOWS + str(id)
		return self.__request(url)

	#Информация об эпизоде
	def episode_info(self, id):
		'''
			Returns information about given episode
		'''
		url = EPISODES + str(id)
		return self.__request(url)

	#TODO Список жанров

	#TODO Рейтинг сериалов

	#TODO Профиль пользователя (другого)

