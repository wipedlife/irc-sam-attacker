from .commands import IRCCommands
import configparser, sys

class handler_msg(IRCCommands):
  # owner_nick=""
  # owner_hostname=""
   def __init__(self, sock):
       config=configparser.ConfigParser()
       config.read("config.ini")

       self.onick=config["OWNER"]["nick"]
       self.ohostname=config["OWNER"]["hostname"]
       self.sock=sock
       #print("Handler is was inited")
       
   def mes_handle(self,msg,to):
       com=msg.split(' ')
      # print("splited (mes_handle): "+str(com))
       if com[0] == "echo" and len(com) > 1 :
           self.privmsg( to, " ".join(com[1:]) )
       if com[0] == "quit" and len(com) > 1:
           self.quit(" ".join(com[1:]))
           sys.exit(0)
   
   def commands(self):
       while True:
           data=self.oread()
           for line in data.split('\n'):
            spl=line.split(' ')
            if ('PONG' in line or 'PING' in line) and (len(spl) == 4 and spl[2] in spl[0] or len(spl) == 2):
                 self.pong(spl[1])
            if len(spl) > 4:
                if spl[1] == 'PRIVMSG': 
                    useri=self.getuser(spl[0])
                    msg=spl[3][1:]
                    print("%s  with hostname %s write message on %s -> %s" %(useri["nick"],useri["host"],spl[2], msg) )
                    if useri["nick"] == self.onick and useri['host'] == self.ohostname:
                     self.mes_handle( line.split(':')[2], spl[2] )
                    
