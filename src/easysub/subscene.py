import os
import urlparse
import zipfile

import requests
from bs4 import BeautifulSoup

from downloader import Downloader
from common import Subtitles, User

class Subscene(object):
	def __init__(self):
		super(Subscene, self).__init__()
		self._base_url = u'http://subscene.com/'
		self._search_url = self._get_full_url(u'/subtitles/title')
		self._cookies = dict(LanguageFilter=u'13')
		self._timeout = 10.0

	def _get_full_url(self, relative_url):
		return urlparse.urljoin(self._base_url, relative_url)

	def _get_soup(self, source):
		return BeautifulSoup(source, u'html.parser')

	def _parse_search_results_source(self, source):
		if not source:
			return list()
		soup = self._get_soup(source)
		subs = list()
		for tr in soup.find(u'tbody').find_all(u'tr'):
			sub = Subtitles()
			tds= tr.find_all(u'td')
			try:
				sub.page_url = self._get_full_url(tds[0].find(u'a')[u'href'])
			except IndexError, e:
				pass
			else:
				try:
					sub.language = tds[0].find_all(u'span')[0].text.strip()
				except IndexError, e:
					pass
				try:
					sub.name = tds[0].find_all(u'span')[1].text.strip()
				except IndexError, e:
					pass
				try:
					sub.files_count = int(tds[1].text.strip()) if tds[1].text.strip() else None
				except IndexError, e:
					pass
				try:
					sub.hearing_impared = True if u'a41' in tds[2][u'class'] else False
				except IndexError, e:
					pass
				try:
					sub.uploader.name = tds[3].find(u'a').text.strip()
					sub.uploader.profile_url = self._get_full_url(tds[3].find('a')['href'])
				except IndexError, e:
					pass
				try:
					sub.comment = tds[4].find(u'div').text.strip()
				except IndexError, e:
					pass
			if sub.page_url:
				subs.append(sub)
		return subs


	def search(self, query):
		if not query:
			return list()
		data = {
			u'q': query,
			u'l': None
		}
		r = requests.get(self._search_url, params=data, cookies=self._cookies, timeout=self._timeout)
		if r.status_code == 200:
			return self._parse_search_results_source(r.text)
			
	def _extract_sub_zip(self, zip_path, sub_path):
		if zipfile.is_zipfile(zip_path):
			try:
				with zipfile.ZipFile(zip_path) as z:
					with z.open(z.namelist()[0]) as sz, open(sub_path, u'wb') as so:
						so.write(sz.read())
				return True
			except Exception, e:
				pass
		return False
		
	def download(self, sub, path):
		r = requests.get(sub.page_url)
		if r.status_code == 200:
			soup = self._get_soup(r.text)
			sub.url = self._get_full_url(
				soup.find(u'a', id=u'downloadButton')[u'href']
			)
			dl = Downloader()
			zip_path = os.path.splitext(path)[0] + u'.zip'
			if dl.download_file(sub.url, zip_path):
				is_extration_success = self._extract_sub_zip(zip_path, path)
				try:
					os.remove(zip_path)
				except OSError, e:
					pass
				if is_extration_success:
					return True
		return False

