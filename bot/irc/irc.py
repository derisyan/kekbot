#!/usr/bin/python
from collections import deque
from num import get_rpl_alias
from time import sleep
import socket
import ssl

def pretty_format_dict(d):
	ret = "{"
	for key in d:
		ret += "\n" + repr(key) + " : " + repr(d[key]) + ","
	ret += "\n}"
	return ret

def unparse_message(msg):
	line = ""
	if msg.prefix:
		line += ":" + msg.prefix + " "
	line += msg.command
	for arg in msg.args:
		line += " " + arg
	if msg.trailing:
		line += " :" + msg.trailing
	line += "\r\n"
	return line

class irc_source:

	def __init__(self, prefix):
		self.raw = prefix
		self.nick = ""
		self.user = ""
		self.host = ""
		if "@" in prefix:
			prefix, self.host = prefix.rsplit("@", 1)
		if "!" in prefix:
			prefix, self.user = prefix.split("!", 1)
		self.nick = prefix

	def __repr__(self):
		return pretty_format_dict(self.__dict__)

	def __str__(self):
		return self.raw

class irc_message:

	def __init__(self, line):
		self.raw = line
		self.prefix = ""
		self.trailing = ""
		self.command = ""
		self.args = []
		if line[0] == ":":
			self.prefix, line = line[1:].split(" ",1)
		if " :" in line:
			line, self.trailing = line.split(" :",1)
		if " " in line :
			self.command, line = line.split(" ",1)
			if " " in line :
				self.args = line.split(" ")
			else:
				self.args = [line,]
		else :
			self.command = line
		self.source = irc_source(self.prefix)


	def __repr__(self):
		return pretty_format_dict(self.__dict__)

	def __str__(self):
		return self.raw

class irc_connection:

	def __init__(self, server, port, nick):
		self._server = server
		self._nick = nick
		self._version = "BYTHON IRC :D:D"
		self.buffer_size = 512
		self.partial_data = ""
		self.print_msg = False
		self.msg_buffer = deque()
		self.init_socket(server, port)
		self.nick(nick)
		self.user(nick.lower())

	def __del__(self):
		self.close_socket()

	def init_socket(self, server, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((server, port))
		self.sock.setblocking(0)

	def close_socket(self):
		self.sock.close()

	def send_raw(self, raw_msg):
		if not raw_msg.endswith("\r\n"):
			raw_msg = raw_msg.strip()
			raw_msg += "\r\n"
		if self.print_msg:
			print(("[>]" + raw_msg))
		self.sock.send(raw_msg)

	def nick(self, new):
		self._nick = new
		self.send_raw("NICK %s" % new)

	def user(self, usr = "user", realname = "realname"):
		self.send_raw("USER %s 0 * :%s" % (usr, realname))

	def privmsg(self, target, msg):
		self.send_raw("PRIVMSG %s :%s" % (target, msg))

	def notice(self, target, msg):
		self.send_raw("NOTICE %s :%s" % (target, msg))

	def ping(self, s1, s2 = ""):
		self.send_raw("PING %s %s" % (s1, s2))

	def pong(self,s1 = "", s2 = ""):
		if s1:
			self.send_raw("PONG %s %s" % (s1, s2))
		else:
			self.send_raw("PONG %s %s" % (self._nick, s2))

	def who(self, nick):
		before_len = len(self.msg_buffer)
		self.send_raw("WHO %s" % nick)
		while True:
			self.recv_msg()
			current_len = len(self.msg_buffer)
			for i in range(0, current_len - before_len):
				msg = irc_message(self.msg_buffer[-1 - i])
				rpl = get_rpl_alias(msg.command)
				if rpl == "whoreply":
					return self.msg_buffer[-1 - i]
				elif rpl == "endofwho":
					return ""
			before_len = current_len

	def join(self, chan):
		if isinstance(chan, str):
			self.send_raw("JOIN %s" % chan)
		elif isinstance(chan, list or tuple):
			self.send_raw("JOIN %s" % ",".join(chan))

	def part(self, chan, msg = "bye"):
		if isinstance(chan, str):
			self.send_raw("PART %s :%s" % (chan, msg))
		elif isinstance(chan, list or tuple):
			self.send_raw("PART %s :%s" % (",".join(chan), msg))

	def quit(self, msg = "ded"):
		self.send_raw("QUIT :%s" % msg)

	def _handle_msg(self, msg):
		global ignored_rpl
		msg = irc_message(msg)
		if msg.command == "PING":
			if msg.trailing.isdigit():
				self.pong(msg.trailing)
			else:
				self.pong()
			return ""
		elif(msg.command == "PRIVMSG") and (msg.trailing == "\x01VERSION\x01"):
			self.notice(msg.source.nick, "\x01VERSION %s\x01" % self._version)
			return ""
		else:
			rpl = get_rpl_alias(msg.command)
			if rpl == "nicknameinuse":
				self._nick += "_"
				self.nick(self._nick)
				return ""
		return msg

	def recv_msg(self):
		try:
			data = self.sock.recv(self.buffer_size)
		except socket.error:
			data = ""
			return
		lines = data.splitlines()
		if len(lines) != 0:
			if self.partial_data:
				lines[0] = lines[0] + self.partial_data
			if not data.endswith("\r\n"):
				self.partial_data = lines.pop()
			else:
				self.partial_data = ""
			for line in lines:
				if self.print_msg:
					print(("[<]" + line))
				tmp = self._handle_msg(line)
				if tmp:
					self.msg_buffer.append(line)

class irc_connection_ssl(irc_connection):
	def init_socket(self, server, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((server, port))
		self.sock = ssl.wrap_socket(self.s)
		self.sock.setblocking(0)

	def close_socket(self):
		self.sock.close()