import json
from HTMLParser import HTMLParser
import urllib2
import threading
import time

html_parser = HTMLParser()

chan_urls = {
	"4chan" : "http://a.4cdn.org/",
	"8chan" : "http://8ch.net/",
	"wiz"   : "http://wizchan.org/",
	"lain"  : "http://lainchan.org/"
}

hdrs = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
	"Accept": "text/html,application/json",
	"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
	"Accept-Encoding": "none",
	"Accept-Language": "en-US,en;q=0.8",
	"Connection": "keep-alive"
}

funposts_dict = {}
funposts_in_progress = []

def strip_html(post):
	search_start = 0
	while(post.find("<",search_start) != -1):
		tag_start = post.find("<",search_start)
		tag_end = post.find(">",tag_start)
		if tag_end == -1 :
			tag_end = len(post) - 2
		post = post.replace(post[tag_start : tag_end+1],"")
		search_start = tag_end + 1
	return post

def find_funposts(post, keyword):
	results = []
	temp = ""
	inside_spoiler = False
	search_start = 0
	while(post.find(keyword, search_start) != -1):
		result_start = post.find(keyword, search_start)
		result_end = result_start
		while(post.find("<", result_end) != -1):
			result_end = post.find("<", result_end)
			if not inside_spoiler:
				if(post[result_end:result_end+22] == "<span class=\"spoiler\">"):
					inside_spoiler = True
				else:
					break
			else:
				if(post[result_end:result_end+7] == "</span>"):
					inside_spoiler = False
				else:
					break
			result_end += 1
		if result_end == result_start:
			result_end = len(post)
		results.append(strip_html(post[result_start : result_end]))
		search_start = result_end
	return results

def get_threads(board, chan):
	global chan_urls, hdrs
	if chan not in chan_urls:
		return []
	try :
		threads_str = urllib2.urlopen(urllib2.Request(chan_urls[chan] + board + "/threads.json", headers = hdrs)).read()
	except urllib2.HTTPError:
		return []
	return json.loads(threads_str)

def get_posts(thread, board, chan):
	global chan_urls, hdrs
	if chan not in chan_urls:
		return []
	posts_url = chan_urls[chan] + board
	if(chan == "4chan"):
		posts_url += "/thread/"
	else:
		posts_url += "/res/"
	posts_url += str(thread["no"]) + ".json"
	try :
		posts_str = urllib2.urlopen(urllib2.Request(posts_url, headers = hdrs)).read()
	except urllib2.HTTPError:
		return []
	return json.loads(posts_str)

def _get_funposts(keyword, board, chan):
	global html_parser, chan_urls
	if chan not in chan_urls:
		return []
	funposts = []
	threads_json = get_threads(board, chan)
	for page in threads_json:
		for thread in page["threads"]:
			posts_json = get_posts(thread, board, chan)
			for post in posts_json["posts"]:
				try:
					clean_post = html_parser.unescape(post["com"]).encode('ascii', 'ignore')
				except:
					continue
				new_funposts = find_funposts(clean_post, keyword)
				funposts += new_funposts
	return funposts

class funpost_thread(threading.Thread):

	def __init__(self, keyword, board, chan):
	    threading.Thread.__init__(self)
	    self.board = board
	    self.chan = chan
	    self.keyword = keyword

	def run(self):
		global funposts_in_progress, funposts_dict
		funposts_in_progress.append((self.keyword, self.board, self.chan))
		try:
			funposts_dict[self.keyword][self.chan][self.board] = _get_funposts(self.keyword, self.board, self.chan)
		except:
			pass
		funposts_in_progress.remove((self.keyword, self.board, self.chan))

def get_funposts(keyword, board, chan):
	global funposts_in_progress, funposts_dict
	if keyword not in funposts_dict:
		funposts_dict[keyword] = {}
	if chan not in funposts_dict[keyword]:
		funposts_dict[keyword][chan] = {}
	if (keyword, board, chan) not in funposts_in_progress:
		t = funpost_thread(keyword, board, chan)
		t.start()
		return 0
	else:
		return 1