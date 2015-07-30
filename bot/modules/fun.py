from core import *
from util import *
from collections import OrderedDict as odict
import random
import re

rainbow_colors = (4, 7, 8, 3, 2, 6, 12)
_spurdo_dict = {
	".":			" :DD",
	",":			" xDD",
	"af":			"ab",
	"ap":			"ab",
	"ca":			"ga",
	"ck":			"gg",
	"co":			"go",
	"ev":			"eb",
	"ex":			"egz",
	"et":			"ed",
	"iv":			"ib",
	"it":			"id",
	"ke":			"ge",
	"nt":			"nd",
	"op":			"ob",
	"ot":			"od",
	"po":			"bo",
	"pe":			"be",
	"up":			"ub",
	"ck":			"gg",
	"cr":			"gr",
	"kn":			"gn",
	"lt":			"ld",
	"mm":			"m",
	"nt":			"dn",
	"pr":			"br",
	"ts":			"dz",
	"te":			"de",
	"tr":			"dr",
	"as":			"az",
	"bs":			"bz",
	"ds":			"dz",
	"fs":			"fz",
	"gs":			"gz",
	"is":			"iz",
	"ls":			"lz",
	"ms":			"mz",
	"ns":			"nz",
	"rs":			"rz",
	"ss":			"sz",
	"se":			"ze",
	"ts":			"tz",
	"us":			"uz",
	"ws":			"wz",
	"ys":			"yz",
#	"ic":			"ig",
	"ng":			"nk",
	"vic":			"vig",
	"wha":			"wa",
	"tha":			"da",
	"thi":			"di",
	"the":			"de",
	"alk":			"olk",
	"ing":			"ign",
	"kek":			"geg",
	"epic":			"ebin",
	"upvote":		"upboat",
	"nice":			"neic"
}
spurdo_dict = odict(sorted(list(_spurdo_dict.items()), key=lambda t: -len(t[0])))

@command("rainbow")
def rainbow(bot, msg, args, pure):
	global rainbow_colors
	tmp = strip_colors(" ".join(args))
	out = "usage: rainbow <text>"
	if tmp:
		out = "\x0F"
		for i in range(0, len(tmp)):
			out += "\x03%02d%s" % (rainbow_colors[i % len(rainbow_colors)], tmp[i])
		out += "\x03"
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("spurdo")
def spurdo(bot, msg, args, pure):
	global spurdo_dict
	tmp = strip_colors(" ".join(args))
	out = "usage: spurdo <text>"
	if tmp:
		tmp_cl = parse_case(tmp)
		tmp = tmp.lower()
		for key in spurdo_dict:
			old_len = len(tmp)
			leftmost = tmp.find(key)
			tmp = tmp.replace(key, spurdo_dict[key])
			offset = len(tmp) - old_len
			tmp_cl = offset_caselist(tmp_cl, leftmost, offset)
		tmp = restore_case(tmp, tmp_cl)
		if tmp.count(":DD") == 0:
			tmp += " :DD"
		for laugh in (":DD", "xDD"):
			laugh_slices = tmp.split(laugh)
			tmp = ""
			if len(laugh_slices) != 1:
				for i in xrange(0, len(laugh_slices)):
					tmp += laugh_slices[i]
					if i < (len(laugh_slices) - 1):
						tmp += laugh[0] + (random.randint(1,4) * "D")
			else:
				tmp = laugh_slices[0]
		out = tmp
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("interject")
def rms_interject(bot, msg, args, pure):
	out = "I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux."
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@trigger("normieblock")
def normie_blocker(bot, msg):
	if (msg.command == "PRIVMSG"):
		if re.search("(my (gf|girlfriend))|(tfw gf)", msg.trailing) is not None:
			bot.conn.privmsg(msg.args[0], "\x0304%s has been blocked for being a normie" % msg.source.nick)