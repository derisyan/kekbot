from core import *
from subprocess import Popen

#This command is for the Raspberry Pi
@command("temp")
def show_temp(bot, msg, args, pure):
	process = Popen(("/opt/vc/bin/vcgencmd", "measure_temp"), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	out = "current temp is " + output.split("=")[-1]
	if (not pure) and out:
		bot.conn.privmsg(msg.args[0], out)
	return out