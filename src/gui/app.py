from PyQt4 import QtGui, QtCore
import sys
import os

from easysub import EasySub, File, FileParser

import ui
import icons


class EasySubThread(QtCore.QThread):
	def __init__(self, files):
		super(EasySubThread, self).__init__()
		self._files = files
		self._easysub = EasySub()
		
	def run(self):
		for i, file in enumerate(self._files):
			self.emit(QtCore.SIGNAL(u'search_started(int)'), i)
			if self._easysub.process_file(file):
				self.emit(QtCore.SIGNAL(u'download_completed(int)'), i)
			else:
				self.emit(QtCore.SIGNAL(u'download_failed(int)'), i)

class EasySubGUI(QtGui.QMainWindow, ui.Ui_dialgEasySub):
	def __init__(self, parent=None):
		super(EasySubGUI, self).__init__(parent)
		self.setupUi(self)
		self._setup_icons()
		
		self._files = list()
		self._file_parser = FileParser()
		self._bg_thread = None
		
		self.btnBrowse.clicked.connect(self.btnBrowse_click)
		self.btnDirectory.clicked.connect(self.btnDirectory_click)
		self.btnDownload.clicked.connect(self.btnDownload_click)
		self.btnClear.clicked.connect(self.btnClear_click)
		
		cmd_file_paths = sys.argv[1:]
		if cmd_file_paths:
			if not self._validate_paths(cmd_file_paths):
				QtGui.QMessageBox.critical(self, u'Oops!', u'Some of the files does not exist.')
			else:
				self.files = self._get_files_from_paths(cmd_file_paths)

	@property
	def files(self):
		return self._files
	
	@files.setter
	def files(self, value):
		self.lstwFiles.clear()
		self._files = value
		for file in self._files:
			self.lstwFiles.addItem(self._get_list_item_from_file(file))
		
	def _setup_icons(self):
		video_icon = QtGui.QIcon()
		video_icon.addFile(u':resources/icons/16x16/video.png', QtCore.QSize(16, 16))
		video_icon.addFile(u':resources/icons/24x24/video.png', QtCore.QSize(24, 24))
		video_icon.addFile(u':resources/icons/32x32/video.png', QtCore.QSize(32, 32))
	
		downloading_icon = QtGui.QIcon()
		downloading_icon.addFile(u':resources/icons/16x16/downloading.png', QtCore.QSize(16, 16))
		downloading_icon.addFile(u':resources/icons/24x24/downloading.png', QtCore.QSize(24, 24))
		downloading_icon.addFile(u':resources/icons/32x32/downloading.png', QtCore.QSize(32, 32))
	
		success_icon = QtGui.QIcon()
		success_icon.addFile(u':resources/icons/16x16/success.png', QtCore.QSize(16, 16))
		success_icon.addFile(u':resources/icons/24x24/success.png', QtCore.QSize(24, 24))
		success_icon.addFile(u':resources/icons/32x32/success.png', QtCore.QSize(32, 32))
	
		failed_icon = QtGui.QIcon()
		failed_icon.addFile(u':resources/icons/16x16/failed.png', QtCore.QSize(16, 16))
		failed_icon.addFile(u':resources/icons/24x24/failed.png', QtCore.QSize(24, 24))
		failed_icon.addFile(u':resources/icons/32x32/failed.png', QtCore.QSize(32, 32))
		
		self._video_icon, self._downloading_icon, self._success_icon, self._failed_icon = \
			video_icon, downloading_icon, success_icon, failed_icon
	
	def btnBrowse_click(self):
		self.btnClear_click()
		files = QtGui.QFileDialog.getOpenFileNames(
			self, u'Select files',
			u'/home', u'Media Files (*.mp4  *.mov  *.avi  *.mkv)'
		)
		if files:
			if not self._validate_paths(files):
				QtGui.QMessageBox.critical(self, u'Error', u'Some of the files does not exist.')
			else:
				self.files = self._get_files_from_paths(files)

	def btnDirectory_click(self):
		self.btnClear_click()
		path = QtGui.QFileDialog.getExistingDirectory(
			self, u'Select directory', u'/home'
		)
		if path:
			if not self._validate_paths([path]):
				QtGui.QMessageBox.critical(self, u'Error', u'The directory you have selected does no exist.')
			else:
				self.files = self._get_files_from_paths([path])

	def btnDownload_click(self):
		if self.files:
			self._bg_thread = EasySubThread(self.files)
			self.connect(self._bg_thread, QtCore.SIGNAL(u'search_started(int)'), self._search_started_callback)
			self.connect(self._bg_thread, QtCore.SIGNAL(u'download_completed(int)'), self._download_completed_callback)
			self.connect(self._bg_thread, QtCore.SIGNAL(u'download_failed(int)'), self._download_failed_callback)
			self.connect(self._bg_thread, QtCore.SIGNAL(u'finished()'), self._finished_callback)
			self._bg_thread.start()
		else:
			QtGui.QMessageBox.critical(self, u'Error', u'No file selected.')

	def btnClear_click(self):
		self.files = list()

	def _search_started_callback(self, file_index):
		item = self.lstwFiles.item(file_index)
		if item:
			item.setIcon(self._downloading_icon)

	def _download_completed_callback(self, file_index):
		item = self.lstwFiles.item(file_index)
		if item:
			item.setIcon(self._success_icon)

	def _download_failed_callback(self, file_index):
		item = self.lstwFiles.item(file_index)
		if item:
			item.setIcon(self._failed_icon)
		
	def _finished_callback(self):
		pass

	def _get_list_item_from_file(self, file):
		return QtGui.QListWidgetItem(
			self._video_icon, file.name + u'.' + file.ext,
			parent=self.lstwFiles, type=QtGui.QListWidgetItem.Type
		)
		
	def _validate_paths(self, paths):
		paths = map(unicode, paths)
		for path in paths:
			if not os.path.exists(path):
				return False
		return True

	def _get_files_from_paths(self, paths):
		paths = map(unicode, paths)
		files = list()
		for path in paths:
				if os.path.isfile(path) and self._file_parser.is_media_file(path):
					try:
						file = File(path=path)
						if not os.path.exists(file.sub_absolute_path):
							files.append(file)
					except UnicodeDecodeError, e:
						pass
				else:
					for item in os.listdir(path):
						try:
							item_path = os.path.join(path, item)
							if os.path.isfile(item_path) and self._file_parser.is_media_file(item_path):
								file = File(path=item_path)
								if not os.path.exists(file.sub_absolute_path):
									files.append(file)
						except UnicodeDecodeError, e:
							pass
		return files


def main():
	app = QtGui.QApplication(sys.argv)
	form = EasySubGUI()
	form.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

