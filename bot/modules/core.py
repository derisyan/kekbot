#!/usr/bin/python

trg_dict = {}
cmd_dict = {}
priv_str = ["blocked", "user", "admin", "owner"]
priv_dict = {"cmd" : {}, "trg" : {}}

def command(name, privilege = 1):
	global cmd_dict, priv_dict
	def self(command_function):
		cmd_dict[name] = command_function
		priv_dict["cmd"][name] = privilege
	return self

def trigger(name, privilege = 1):
	global trg_dict, priv_dict
	def self(trigger_function):
		trg_dict[name] = trigger_function
		priv_dict["trg"][name] = privilege
	return self