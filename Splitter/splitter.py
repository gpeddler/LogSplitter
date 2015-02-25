import os, re, glob, tarfile, shutil
from datetime import datetime

SPLIT_FILE = './log_splitter.log'

class Splitter:

	def start(self, location_target, location_finish, regex, time_str):
		self.location_finish = location_finish
		self.year_top = 0
		self.month_top = 0

		print "START SPLITTER :: " + location_target + " >> " + location_finish

		os.rename(location_target, SPLIT_FILE)

		if(not os.path.exists(location_finish)):
			os.mkdir(location_finish)

		file = open(SPLIT_FILE, 'r')
		lines = file.readlines()

		for line in lines:
			self.make_files(self.get_match(line, regex), line, time_str)

		self.compress()
		file.close()

		os.remove(SPLIT_FILE)

	def get_match(self, data, regex):

		# PARSING LOG FILE

		# regex = re.compile(
		#     r"""
		# 	    (?P<ip>.*?)\s-\s-\s
		# 	    \[(?P<date>.*?)\]\s
		# 	    \'(?P<msg>.*?)\'\s
		# 	    (
		# 	    	  \d\d\d\s-\s\'-\'\s 
		# 	    	| \d\d\d\s\d+\s
		#     	)
		# 	    \'(?P<media>.*?)\'
		#     """, re.VERBOSE)

		# regex = re.compile(
		#     r"""
		# 	    (?P<date>.*?)\s
		# 	    (?P<date>.*?)\s
		# 	    \[error\]\s
		# 	    \d+#\d:\s\*\d+\sconnect\(\)\sfailed\s
		# 	    (?P<connect>.*?)\s
		# 	    .*?,\s
		# 	    client:\s(?P<client>.*?),\s
		# 	    server:\s(?P<server>.*?),\s
		# 	    request:\s"(?P<request>.*?)
		# 	    '(?P<msg>.*?)\'\s
		# 	    (
		# 	    	  \d\d\d\s-\s\'-\'\s 
		# 	    	| \d\d\d\s\d+\s
		#     	)
		# 	    \'(?P<media>.*?)\'
		#     """, re.VERBOSE)

		regex_complie = re.compile(regex, re.VERBOSE)
		match = regex_complie.match(data)

		return match

	def make_files(self, match, data, time_str):
		# date = datetime.strptime(match.group('date'), '%d/%b/%Y:%H:%M:%S')
		date = datetime.strptime(match.group('date'), time_str)
		
		if date.year > self.year_top:
			self.year_top = date.year
		if date.month > self.month_top:
			self.month_top = date.month

		# SETTING DIRCTORY
		dir_name = str(date.strftime('%Y-%m'))
		dir_location = self.location_finish + '/' + dir_name

		if(not os.path.exists(dir_location)):
			os.mkdir(dir_location)

		# MAKE FILES
		file_name = str(date.strftime('%Y-%m-%d'))
		file_txt = open(dir_location + '/' + file_name, 'a')

		file_txt.write(data)
		file_txt.close()

	def compress(self):
		print "COMPRESS :: ZIP"

		target_dirs = []

		for root, dirs, files in os.walk(self.location_finish):
			if len(files) > 0:
				if int(files[0][:4]) != self.year_top or int(files[0][5:7]) != self.month_top:
					target_dir = self.location_finish + '/' + files[0][:7]
					self.make_tarfile(target_dir + ".tar.gz", root)
					shutil.rmtree(target_dir)

	def make_tarfile(self, output_filename, source_dir):
	    with tarfile.open(output_filename, "w:gz") as tar:
	        tar.add(source_dir, arcname=os.path.basename(source_dir))

