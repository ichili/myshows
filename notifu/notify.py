import subprocess
import ntpath

def notify(message, title='MyShows', delay=5):
	message = str(message)
	path = ntpath.dirname(__file__)
	params = []
	params.append(ntpath.join(path, 'notifu.exe'))
	params.extend(['/m', message])
	params.extend(['/p', title])
	params.extend(['/d', str(delay)])
	params.extend(['/i', 'favicon.ico'])
	subprocess.Popen(params)