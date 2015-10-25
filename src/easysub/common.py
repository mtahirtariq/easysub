import os


class File():
	def __init__(self, path=None):
		self.absolute_path = None
		self.directory = None
		self.name = None
		self.ext = None
		self.sub_absolute_path = None
		if path:
			self.absolute_path = path
			self.directory = os.path.dirname(self.absolute_path)
			self.name, self.ext = \
				os.path.splitext(os.path.basename(self.absolute_path))
			self.sub_absolute_path = os.path.join(self.directory, self.name + u'.srt')			


class User(object):
	def __init__(self):
		self.name = None
		self.profile_url = None


class Subtitles(object):
	def __init__(self):
		self.page_url = None
		self.url = None
		self.language = None
		self.name = None
		self.files_count = None
		self.hearing_impared = None
		self.uploader = User()
		self.comment = None

