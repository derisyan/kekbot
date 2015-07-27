from core import *
import random

dice_operators = ("+", "-")

eightball_phrases = (
	"signs point to yes",
	"yes",
	"reply hazy, try again",
	"without a doubt",
	"my sources say no",
	"as i see it, yes",
	"you may rely on it",
	"concentrate and ask again",
	"outlook not so good",
	"it is decidedly so",
	"better not tell you now",
	"very doubtful",
	"yes - definitely",
	"it is certain",
	"cannot predict now",
	"most likely",
	"ask again later",
	"my reply is no",
	"outlook good",
	"don't count on it"
)

def parse_dice_notation(s):
	global dice_operators
	err_start = "\x1F"
	err_end = err_start
	before_d = True
	current_dice = [0,0]
	parsed = []
	for i in xrange(0, len(s)):
		c = s[i]
		if c.isdigit():
			if before_d:
				tmp = 0
			else:
				tmp = 1
			current_dice[tmp] = (current_dice[tmp] * 10) + int(c)
		elif c == "d":
			if before_d:
				before_d = False
			else:
				return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
		elif (c == " ") or (c in dice_operators):
			if 0 not in current_dice:
				parsed.append(current_dice)
				current_dice = [0, 0]
				before_d = False
			elif (current_dice[0] != 0) and (current_dice[1] == 0):
				if before_d:
					parsed.append(current_dice[0])
					current_dice = [0, 0]
				else:
					return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
			elif (current_dice[0] == 0) and (current_dice[1] != 0):
				parsed.append([1, current_dice[1]])
				current_dice = [0, 0]
			if c != " ":
				# TODO :: MAKE THIS EXPLICIT FOR THE MUL AND DIV OPERATORS
				if len(parsed) == 0:
					return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
				elif parsed[-1] in dice_operators:
					return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
				if parsed[-1] == " ":
					parsed.pop()
			else:
				if (len(parsed) == 0) or (parsed[-1] in dice_operators) or (parsed[-1] == " "):
					before_d = True
					continue
			parsed.append(c)
			before_d = True
		else:
			return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
	if 0 not in current_dice:
		parsed.append(current_dice)
		current_dice = [0, 0]
	elif (current_dice[0] != 0) and (current_dice[1] == 0):
		if before_d:
			parsed.append(current_dice[0])
			current_dice = [0, 0]
		else:
			return "error: " + s[:i] + err_start + c + err_end + s[i+1:]
	return parsed

def roll_parsed(parsed):
	global operators
	if isinstance(parsed,str):
		return parsed
	elif parsed == []:
		return "error: no result"
	seperator = " \x0303::\x03 "
	results = []
	maximums = []
	ret = ""
	last_op = "+"
	tmp_ret = ""
	tmp_result = 0
	tmp_max = 0
	parsed.append(" ")
	for element in parsed:
		curr_result = 0
		curr_max = 0
		if isinstance(element, list):
			if (element[0] > 20) or (element[1] > 100):
				curr_result = 0
				curr_max = 0
			else:
				tmp_ret += (" %s " % last_op)
				for i in xrange(0, element[0]):
					tmp = random.randint(1, element[1])
					tmp_ret += str(tmp) + ","
					curr_result += tmp
				tmp_ret = tmp_ret[:-1]
				tmp_ret += "(d%s)" % element[1]
				curr_max += element[0] * element[1]
		elif isinstance(element, int):
			curr_result += element
			curr_max += element
			tmp_ret += (" %s " % last_op) + str(element)
		elif isinstance(element, str):
			if element == " ":
				tmp_ret += " / " + str(tmp_max) + seperator
				if tmp_ret[:3] == " + ":
					tmp_ret = tmp_ret[3:]
				ret += tmp_ret
				tmp_ret = ""
				results.append(str(tmp_result))
				maximums.append(str(tmp_max))
				tmp_result = 0
				tmp_max = 0
			elif element in operators:
				last_op = element
		if last_op == "+":
			tmp_result += curr_result
			tmp_max += curr_max
		elif last_op == "-":
			tmp_result -= curr_result
			tmp_max -= curr_max
	ret = ",".join(results) + seperator + ret
	return ret

@command("roll")
def roll(bot, msg, args, pure):
	out = "usage: roll <dice_notation>"
	if len(args) != 0:
		tmp = " ".join(args)
		out = msg.source.nick + ": " + roll_parsed(parse_dice_notation(tmp))
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("8ball")
def eightball(bot, msg, args, pure):
	global eightball_phrases
	out = msg.source.nick + ": " + random.choice(eightball_phrases)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out