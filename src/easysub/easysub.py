import os

import requests

from fileparser import FileParser
from subscene import Subscene
from common import File


class EasySub(object):
	def __init__(self):
		super(EasySub, self).__init__()
		self._file_parser = FileParser()
		self._subscene = Subscene()

	def _get_search_term(self, file):
		return u' '.join(self._file_parser.parse_filename(file.name))
		
	def process_file(self, file):
		search_term = self._get_search_term(file)
		try:
			results = self._subscene.search(search_term)
		except Exception, e:
			pass
		else:
			if results:
				valid_sub = results[0]
				try:
					if self._subscene.download(valid_sub, file.sub_absolute_path):
						return True
				except Exception, e:
					pass
		return False

