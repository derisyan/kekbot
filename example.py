from bot import irc_bot

kekbot = irc_bot("irc.rizon.net", 9999, "kekbot", True)
kekbot.conn.print_msg = True
kekbot.set_privilege("AtaK", 3)
while True:
	kekbot.loop()
