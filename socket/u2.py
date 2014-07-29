from sockchat import sockchat

chat = sockchat()
uid = chat.connectServ("user2")
print uid
chat.sendChat("user1","hello user1, i am user2")
chat.closeServ()