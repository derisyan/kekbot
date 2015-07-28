from core import *

@command("join", 2)
def join(bot, msg, args, pure):
	out = "usage: join <chans> "
	if len(args) > 0:
		for chan in args:
			bot.conn.join(chan)
		out = "joined %s" % ", ".join(args)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("part", 2)
def part(bot, msg, args, pure):
	out = "usage: part [chans]"
	if (len(args) == 0) and ("#" in msg.args[0]):
		bot.conn.part(msg.args[0])
	elif len(args) > 0:
		for chan in args:
			bot.conn.part(chan)
		out = "parted from %s" % ", ".join(args)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("setpr", 3)
def setpr(bot, msg, args, pure):
	out = "usage: setpr <nick> <priv>"
	if (args[1].isdigit()) and (len(args) != 2):
		p = int(args[1])
		if (p < 0) and (p > 3):
			out = "error: invalid privilege"
		else:
			bot.set_privilege(args[0], p)
			out = "\x0F%s's privilege set to %s" % (args[0], priv_str[p])
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("block", 2)
def block(bot, msg, args, pure):
	out = "usage: block <nicks>"
	if len(args) != 0:
		for n in args:
			bot.set_privilege(n, 0)
		out = "blocked %s" % ", ".join(args)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("unblock", 2)
def unblock(bot, msg, args, pure):
	out = "usage: unblock <nicks>"
	if len(args) != 0:
		for n in args:
			bot.set_privilege(n, 1)
		out = "unblocked %s" % ", ".join(args)
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("nick", 3)
def nick(bot, msg, args, pure):
	out = "usage: nick <nick>"
	if len(args) == 1:
		bot.bot.conn.nick(args[0])
		out = ""
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("commands", 2)
def list_commands(bot, msg, args, pure):
	out = "usage: commands <add/del/list> [cmds]"
	if len(args) >= 1:
		if args[0] == "list":
			tmp = "cmds: "
			for cmd in cmd_dict:
				if cmd in bot.active_cmd:
					tmp += "\x0303"
				else:
					tmp += "\x0304"
				tmp += cmd + " "
			out = tmp
		elif (args[0] == "add") and len(args) > 1:
			tmp = []
			for cmd in args[1:]:
				if (cmd in cmd_dict) and (cmd not in bot.active_cmd):
					bot.active_cmd.append(cmd)
					tmp.append(cmd)
			out = "cmds added: %s" % ", ".join(tmp)
		elif (args[0] == "del") and len(args) > 1:
			tmp = []
			for cmd in args[1:]:
				if (cmd in cmd_dict) and (cmd in bot.active_cmd):
					bot.active_cmd.remove(cmd)
					tmp.append(cmd)
			out = "cmds del'd: %s" % ", ".join(tmp)
		if (not pure) and out:
			bot.conn.privmsg(msg.args[0], out)
		return out

@command("triggers", 2)
def list_triggers(bot, msg, args, pure):
	out = "usage: triggers <add/del/list> [cmds]"
	if len(args) >= 1:
		if args[0] == "list":
			tmp = "trgs: "
			for trg in trg_dict:
				if trg in bot.active_trg:
					tmp += "\x0303"
				else:
					tmp += "\x0304"
				tmp += trg + " "
			out = tmp
		elif (args[0] == "add") and len(args) > 1:
			tmp = []
			for trg in args[1:]:
				if (trg in trg_dict) and (trg not in bot.active_trg):
					bot.active_trg.append(trg)
					tmp.append(trg)
			out = "trgs added: %s" % ", ".join(tmp)
		elif (args[0] == "del") and len(args) > 1:
			tmp = []
			for trg in args[1:]:
				if (trg in trg_dict) and (trg in bot.active_trg):
					bot.active_trg.remove(trg)
					tmp.append(trg)
			out = "trgs del'd: %s" % ", ".join(tmp)
		if (not pure) and out:
			bot.conn.privmsg(msg.args[0], out)
		return out

@command("cmdprefix", 3)
def set_cmd_prefix(bot, msg, args, pure):
	tmp = " ".join(args)
	out = "usage: cmdprefix <command prefix>"
	if tmp:
		bot.cmd_prefix = tmp
		out = "set cmd_prefix to '%s'" % tmp
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("cooldown", 3)
def set_cooldown(bot, msg, args, pure):
	out = "usage: cooldown <float(secs)>"
	if (len(args) == 1) and args[0].isdigit():
		tm = float(args[0])
		if (tm > 0) and (tm < 61):
			bot.cooldown_time = tm
			out = "cooldown set to %f seconds" % tm
		else:
			out = "cooldown value too extreme: %f" % tm
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out