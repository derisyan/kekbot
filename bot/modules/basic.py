from core import *

@trigger("ibip")
def ibip_response(bot, msg):
	if (msg.command == "PRIVMSG") and (msg.trailing.rstrip() == ".bots"):
		bot.conn.privmsg(msg.args[0], "Reporting in! [Python] See %shelp for help" % bot.cmd_prefix)

@command("test")
def test(bot, msg, args, pure):
	out = "Hello, %s" % msg.source.nick
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("help")
def help(bot, msg, args, pure):
	cmd_list = []
	for cmd in bot.active_cmd:
		if bot.get_privilege(msg.source.nick) >= priv_dict["cmd"][cmd]:
			cmd_list.append(cmd)
	out = "cmds available to %s: %s" % (msg.source.nick, ", ".join(cmd_list))
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out

@command("showpr")
def showpr(bot, msg, args, pure):
	if len(args) == 0:
		args.append(msg.source.nick)

	if len(args) > 1:
		out = "usage: showpr [nick]"
	else:
		out = "\x0F%s is %s" % (args[0], priv_str[bot.get_privilege(args[0])])
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out