from irc import *
import time
from modules import *

class command_error(Exception):

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return "command_error: %s" % self.msg

def parse_cmd(line):
	line = line.strip()
	if " " in line:
		cmd, line = line.split(" ", 1)
		args = line.split()
		return (cmd, args)
	else:
		return (line, [])

class irc_bot:

	def __init__(self, server, port, nick, ssl = False):
		if ssl:
			self.conn = irc.irc_connection_ssl(server, port, nick)
		else:
			self.conn = irc.irc_connection(server, port, nick)
		self.cmd_prefix = "."
		self.last_ping = 0
		self.ping_interval = 100
		self.desired_loop_tm = 0.15
		self.cooldown_time = 5
		self.user_dict = {}
		self.active_cmd = list(core.cmd_dict.keys())
		self.active_trg = list(core.trg_dict.keys())

	def set_privilege(self, nick, priv):
		if (priv < 0) or (priv > 3):
			return -1
		self.store_user(irc.irc_source(nick))
		self.user_dict[nick]["privilege"] = priv

	def get_privilege(self, nick):
		if nick in self.user_dict:
			return self.user_dict[nick]["privilege"]
		else:
			return 1

	def check_privilege(self, nick, priv):
		tmp = self.get_privilege(nick)
		if (priv > 1) and (tmp > 1):
			msg = self.conn.who(nick)
			if not msg:
				return False
			msg = irc.irc_message(msg)
			if "r" not in msg.args[6]:
				tmp = 1
		return (tmp >= priv)

	def check_blocked(self, nick):
		return (self.get_privilege(nick) == 0)

	def check_cooldown(self, nick, cur):
		self.store_user(irc.irc_source(nick))
		if((cur - self.user_dict[nick]["cooldown"]) > self.cooldown_time):
			self.user_dict[nick]["cooldown"] = cur
			return False
		else:
			return True

	def store_user(self, src):
		if src.nick not in self.user_dict:
			self.user_dict[src.nick] = {
				"host" : [],
				"privilege" : 1,
				"cooldown" : 0
			}
		if src.host and (src.host not in self.user_dict[src.nick]["host"]):
			self.user_dict[src.nick]["host"].append(src.host)

	def do_cmd(self, msg, cmd, args, pure = False):
		if cmd not in core.cmd_dict:
			raise command_error("command not found")
		elif cmd not in self.active_cmd:
			raise command_error("command deactivated")
		elif not self.check_privilege(msg.source.nick, core.priv_dict["cmd"][cmd]):
			raise command_error("not enough privilege")
		else:
			return core.cmd_dict[cmd](self, msg, args, pure)

	def do_trg(self, msg, trg):
		if trg in core.trg_dict:
			if self.check_privilege(msg.source.nick, core.priv_dict["trg"][trg]):
				core.trg_dict[trg](self, msg)

	def loop(self):
		self.conn.recv_msg()
		start_cl = time.clock()
		start_tm = time.time()
		if (start_tm - self.last_ping) > self.ping_interval:
			self.conn.ping(self.conn._server)
			self.last_ping = start_tm
		while len(self.conn.msg_buffer) > 0:
			msg = irc.irc_message(self.conn.msg_buffer.popleft())
			if (msg.command == "PRIVMSG"):
				if msg.args[0] == self.conn._nick:
					msg.args[0] = msg.source.nick
			if self.check_blocked(msg.source.nick):
				continue
			elif self.get_privilege(msg.source.nick) <= 1:
				if self.check_cooldown(msg.source.nick, start_tm):
					continue
			for trg in self.active_trg:
				self.do_trg(msg, trg)
			if (msg.command == "PRIVMSG") and (msg.trailing[:len(self.cmd_prefix)] == self.cmd_prefix):
				msg.trailing = msg.trailing[len(self.cmd_prefix):]
				if "|" in msg.trailing: # piped commands
					exprs = [x.strip() for x in msg.trailing.split("|")]
					tmp = ""
					if "" not in exprs:
						for i in range(0, len(exprs)):
							e = exprs[i]
							if tmp:
								e += " " + tmp
							cmd, args = parse_cmd(e)
							try:
								tmp = self.do_cmd(msg, cmd, args, (i != (len(exprs) - 1)))
							except command_error as err:
								#self.conn.privmsg(msg.args[0], "%s: %s: %s" % (msg.source.nick, err.msg, cmd))
								break
					else:
						self.conn.privmsg(msg.args[0], "%s: parse error near '|'" % msg.source.nick)
				else:
					cmd, args = parse_cmd(msg.trailing)
					try:
						self.do_cmd(msg, cmd, args)
					except command_error as err:
						pass #self.conn.privmsg(msg.args[0], "%s: %s: %s" % (msg.source.nick, err.msg, cmd))
		end_cl = time.clock()
		sleep_tm = self.desired_loop_tm - (end_cl - start_cl)
		if sleep_tm > 0:
			time.sleep(sleep_tm)