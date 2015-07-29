from core import *
from chanapi import *
import random

DEFAULT_BOARD = "r9k"
DEFAULT_CHAN = "8chan"
keywords = ("tfw","implying")
for kw in keywords:
	funposts_dict[kw] = {}
	for chan in chan_urls:
		funposts_dict[kw][chan] = {}

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

def arg_check(cmd_args):
	global DEFAULT_CHAN
	if len(cmd_args) > 2:
		return None
	elif len(cmd_args) == 2:
		return (cmd_args[0], cmd_args[1])
	elif len(cmd_args) == 1:
		return (cmd_args[0], DEFAULT_CHAN)
	else:
		return (DEFAULT_BOARD, DEFAULT_CHAN)

@command("re-feel", 2)
def re_feel(bot, msg, args, pure):
	global chan_urls
	out = "usage:  re-feel <board> <chan>"
	if arg_check(args) is not None:
		board, chan = arg_check(args)
		if chan not in chan_urls:
			out = "unknown chan: %s " % chan
		else:
			tmp = get_funposts("tfw", board, chan)
			if not tmp:
				out = "scraping feels from %s /%s/" % (chan, board)
			else:
				out = "already scraping %s /%s/" % (chan, board)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("feel")
def feel(bot, msg, args, pure):
	global chan_urls, funposts_in_progress
	out = "usage: feel <board> <chan>"
	if arg_check(args) is not None:
		board, chan = arg_check(args)
		if chan not in chan_urls:
			out = "unknown chan: %s " % chan
		elif ("tfw", board, chan) in funposts_in_progress:
			out = "still scraping %s /%s/" % (chan, board)
		elif board not in funposts_dict["tfw"][chan]:
			out = "board not scraped: %s /%s/" % (chan, board)
		elif funposts_dict["tfw"][chan][board] != []:
			out = "\x0303>%s" % (random.choice(funposts_dict["tfw"][chan][board]))
		else:
			out = "no feels found: %s /%s/" % (chan, board)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("re-imply",2)
def re_imply(bot, msg, args, pure):
	global chan_urls
	out = "usage:  re-imply <board> <chan>"
	if arg_check(args) is not None:
		board, chan = arg_check(args)
		if chan not in chan_urls:
			out = "unknown chan: %s " % chan
		else:
			tmp = get_funposts("implying", board, chan)
			if not tmp:
				out = "scraping implications from %s /%s/" % (chan, board)
			else:
				out = "already scraping %s /%s/" % (chan, board)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("imply")
def imply(bot, msg, args, pure):
	global chan_urls, funposts_in_progress
	out = "usage: imply <board> <chan>"
	if arg_check(args) is not None:
		board, chan = arg_check(args)
		if chan not in chan_urls:
			out = "unknown chan: %s " % chan
		elif ("implying", board, chan) in funposts_in_progress:
			out = "still scraping %s /%s/" % (chan, board)
		elif board not in funposts_dict["tfw"][chan]:
			out = "board not scraped: %s /%s/" % (chan, board)
		elif funposts_dict["tfw"][chan][board] != []:
			out = "\x0303>%s" % (random.choice(funposts_dict["implying"][chan][board]))
		else:
			out = "no implications found: %s /%s/" % (chan, board)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out