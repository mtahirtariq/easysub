import re


class FileParser(object):
	def __init__(self):
		pass

	def parse_filename(self, filename):
		return re.findall(r"[\w']+", filename)

	def is_media_file(self, filepath):
		media_exts = (u'.mp4', u'.mov', u'.avi', u'.mkv')
		if filepath:
			return filepath.endswith(media_exts)
		return False

