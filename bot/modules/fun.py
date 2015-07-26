from core import *
from string import digits
from collections import OrderedDict as odict

rainbow_colors = (4, 7, 8, 3, 2, 6, 12)
_spurdo_dict = {
	".":			" :DD",
	",":			" xDD",
	"th":			"d",
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
	"ts":			"tz",
	"us":			"uz",
	"ws":			"wz",
	"ys":			"yz",
	"ic":			"ig",
	"ng":			"nk",

	"wha":			"wa",
	"alk":			"olk",
	"ing":			"ign",
	"kek":			"geg",
	"epic":			"ebin",
	"upvote":		"upboat",
	"nice":			"neic"
}
spurdo_dict = odict(sorted(list(_spurdo_dict.items()), key=lambda t: -len(t[0])))

def parse_color_text(text):
	if "\x03" not in text:
		return [("", "", text)]
	pieces = text.split("\x03")
	tmp = []
	while "" in pieces:
		pieces.remove("")
	for p in pieces:
		fg_str = ""
		bg_str = ""
		past_comma = False
		counter = 3
		for i in range(0, 6):
			if counter <= 0:
				break
			if p[i] in digits:
				if not past_comma:
					fg_str += p[i]
				else :
					bg_str += p[i]
			elif (p[i] == ",") and (not past_comma):
				past_comma = True
				counter = 3
			else:
				break
			counter -= 1
		p = p[i:]
		fg, bg = -1, -1
		print((fg_str,"|",bg_str))
		if fg_str:
			fg = int(fg_str)
			fg_str,"->",fg
		if bg_str:
			bg = int(bg_str)
		tmp.append((fg, bg, p))
	return tmp

def colorize_text(text, fg = -1, bg = -1):
	tmp = ""
	if (fg != -1) or (bg != -1):
		tmp += "\x03"
	else:
		return text
	if fg != -1:
		tmp += "%02d" % fg
	if bg != -1:
		tmp += ",%02d" % bg
	tmp += text
	return tmp

def unparse_color_text(parsed):
	tmp = ""
	for p in parsed:
		tmp += p[2]
	return tmp

def strip_colors(text):
	tmp = ""
	for p in parse_color_text(text):
		tmp += p[2]
	return tmp

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
		tmp = tmp.lower()
		for key in spurdo_dict:
			tmp = tmp.replace(key, spurdo_dict[key])
		if tmp.count(":DD") == 0:
			tmp += " :DDD"
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
