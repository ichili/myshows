class Error(Exception):

	def __init__(self):
		self.message = ''

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return self.message		

class NotFoundError(Error):
	
	def __init__(self, *args):
		self.message = 'Not found'

class AuthorizationRequiredError(Error):
	
	def __init__(self, *args):
		self.message = 'Authorization required'

class AuthorizationError(Error):
	
	def __init__(self, *args):
		self.message = 'Login or password is not valid'

class MissingParameterError(Error):
	
	def __init__(self, *args):
		self.message = 'One or more parameters are missing'

class WrongParametersError(Error):
	
	def __init__(self, *args):
		self.message = 'Not supproted parameter'

class UnknownError(Error):
	
	def __init__(self, *args):
		self.message = 'Unknown error'