from .commands import IRCCommands
import configparser, sys, asyncio

class handler_msg(IRCCommands):
  # owner_nick=""
  # owner_hostname=""
   def __init__(self, sock):
       config=self.read_cfg()
       self.onick=config["OWNER"]["nick"]
       self.ohostname=config["OWNER"]["hostname"]
       self.sock=sock

       #print("Handler is was inited")
       
   async def mes_handle(self,msg,to):
       com=msg.split(' ')
      # print("splited (mes_handle): "+str(com))
       if com[0] == "echo" and len(com) > 1 :
           self.privmsg( to, " ".join(com[1:]) )
       if com[0] == "quit" and len(com) > 1:
           self.quit(" ".join(com[1:]))
           sys.exit(0)
       if "whois_channels" in com[0] and len(com) > 1:
           channels=self.getChannels(com[1])
           self.privmsg(  "Channels of him: %s" %s ( str(channels) ) )


   async def handl(self,choose=""):
       data = self.oread()
       for line in data.split('\n'):
           spl = line.split(' ')
           if ('PONG' in line or 'PING' in line) and (len(spl) == 4 and spl[2] in spl[0] or len(spl) == 2):
               self.pong(spl[1])
           if len(spl) > 4:
               if spl[1] == 'PRIVMSG':
                   useri = self.getuser(spl[0])
                   msg = spl[3][1:]
                   print("%s  with hostname %s write message on %s -> %s" % (useri["nick"], useri["host"], spl[2], msg))
                   if useri["nick"] == self.onick and useri['host'] == self.ohostname:
                       await self.mes_handle(line.split(':')[2], spl[2])
           #print("Line: %s" % (line))
           if len(spl) >= 3 and spl[1] == 'NICK':
            print("Choose: Y %s" %(choose))
            if 'NICK' in line:
                print("New nick is %s " % (spl))
                return True, spl[2][1:]
       return False, ""

   async def commands(self):
           await self.handl()
           #try:
           # loop = asyncio.get_event_loop()
           # loop.call_soon(commands, loop)
           #...
                    
