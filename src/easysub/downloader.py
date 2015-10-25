import requests


class Downloader(object):
	def __init__(self):
		pass
		
	def download_file(self, url, path):
		try:
			r = requests.get(url, stream=True)
			if r.status_code == 200:
				with open(path, u'wb') as f:
					for chunk in r.iter_content(1024):
						if chunk:
							f.write(chunk)
				return True
		except Exception, e:
			pass
		return False

