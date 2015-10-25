import os
import sys

from fileparser import FileParser
from common import File
from easysub import EasySub


class EasySubConsole(object):
	def __init__(self):
		super(EasySubConsole, self).__init__()
		self._file_parser = FileParser()
		self._easysub = EasySub()

	def _usage(self):
		return u"""Usage:
	main.py path [path, ...]
	
	path:    File or directory's absolute path
		"""
		
	def _exit(self, code=0):
		sys.exit(code)

	def _validate_paths(self, paths):
		for path in paths:
			if not os.path.exists(path):
				return False
		return True

	def _get_files_from_paths(self, paths):
		files = list()
		for path in paths:
			if os.path.isfile(path) and self._file_parser.is_media_file(path):
				file = File(path=path)
				if not os.path.exists(file.sub_absolute_path):
					files.append(file)
			else:
				for item in os.listdir(path):
					item_path = os.path.join(path, item)
					if os.path.isfile(item_path) and self._file_parser.is_media_file(item_path):
						file = File(path=item_path)
						if not os.path.exists(file.sub_absolute_path):
							files.append(file)
		return files

	def run(self, args):
		if not args:
			print self._usage()
			self._exit(1)
		if not self._validate_paths(args):
			print u'Some of the input paths are not valid.'
			self._exit(2)
		files = self._get_files_from_paths(args)
		files_n = len(files)
		print unicode(files_n) + u' media files without subtitles found!'
		for file in files:
			if self._easysub.process_file(file):
				print os.path.basename(file.sub_absolute_path) + u' is available.'
			else:
				print os.path.basename(file.sub_absolute_path) + u' could not be downloaded.'
		self._exit(0)


def main():
	EasySubConsole().run(sys.argv[1:])


if __name__ == u'__main__':
	main()

