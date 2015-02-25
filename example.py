from splitter import Splitter

location_target = './Log/error.log'
location_finish = './Log/log_error'
regex = r"""
		    (?P<date>.*?)\s
		    .*?
	    """
time_str = '%Y/%m/%d';

splitter = Splitter()
splitter.start(location_target, location_finish, regex, time_str)
