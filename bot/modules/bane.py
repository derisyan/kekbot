from core import *
import random
import re

baneposting_dict = {
	"(doctor|dr\.?) pavel i(\'|\ a)?m cia": "he wasn't alone",
	"he wasn\'?t alone": "uh, you don't get to bring friends",
	"(yo)?u don\'?t get to bring ": "they are not my friends!",
	"no charge for them": "and why would i want them",
	"[wh]?y would i want them": "they were trying to grab ya prize, they work for the mercenary, the masketta man",
	"they work for the mercenary,? the (masketta|masked) man": "bane?!",
	"bane\?!?": "aye",
	"^aye": "get em on board, i'll call it in",
	"who ordered you to grab (doctor|dr\.?) pavel": "",
	"tell me about bane,? why does he wear the mask": "",
	"(lot of|lotta) loyalty for a hired gun": "or perhaps he's wondering why someone would shoot a man, before throwing him out of a plane?",
	"or perhaps he\'s wondering why someone would shoot a man,? before throwing him out of a plane": "at least you can talk, who are you?",
	"at least you can talk,? who (are|r) (yo)?u": "it doesn't matter who we are, what matters is our plan",
	"no one cared who i was (till|until) i put on the mask": "if i pull that off will you die?",
	"if i pull that off will (yo)?u die": "it would be extremely painful",
	"it( would|\'d) be extremely painful": "you're a big guy",
	"(yo)?u(\'?re?|\ are) a big guy": "for you",
	"was getting caught part of (yo)?ur plan": "of courshe",
	"what\'?s the next step of (yo)?ur master plan": "crashing this plane... with no survivors!",
	"crashing this plane.{0,4} with no survivors!": "no, this can't be happening! i'm in charge here!",
	"they expect one of us in the wreckage brother": "have we started the fire?",
	"have we started the fire": "yes, the fire rises",
}

@trigger("banepost")
def bane_trg(bot, msg):
	global baneposting_dict
	if (msg.command == "PRIVMSG"):
		for key in baneposting_dict:
			if re.search(key, msg.trailing.lower()) is not None:
				bot.conn.privmsg(msg.args[0], baneposting_dict[key])
				break