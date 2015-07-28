#!/usr/bin/python

def parse_case(text):
	tmp = []
	for i in xrange(0, len(text)):
		if text[i].isupper():
			tmp.append(i)
	return tmp

def offset_caselist(cl, left, offset):
	if (len(cl) == 0) or (left > cl[-1]):
		return cl
	for i in xrange(0, len(cl)):
		if cl[i] >= left:
			break
	for j in xrange(i, len(cl)):
		cl[j] += offset
	return cl

def restore_case(text, cl):
	text = list(text)
	for e in cl:
		try:
			text[e] = text[e].upper()
		except IndexError:
			break
	text = "".join(text)
	return text

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
			if p[i].isdigit():
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

def is_float(text):
	if (text.count(".") == 0) and (text.isdigit()):
		return True
	elif (text.count(".") == 1) and (text.find(".") not in (0, (len(text) - 1))):
		return True
	else:
		return False
