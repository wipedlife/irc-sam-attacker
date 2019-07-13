from .commands import IRCCommands
from .handler_msg import handler_msg as handler
from leaflet import Controller as SAM
import time

class IRCOverlay(IRCCommands):
   samd=None           
   hand=None
   def ping_pong(self):
           MAXREAD=30 # OverKill
           ST=1
           
           for i in range(1,MAXREAD):
               try:
                data=self.oread()
               except TimeoutError:
                   print("Ping-pong timeout, I will ignore it")
                   return False
               for line in data.split('\n'):
                  # print ("Ping_Pong line - " + line)
                   if 'PING' in line:
                       splited=line.split(" ")
                       if len(splited )>1:
                        self.pong(splited[1])
                        return True
                       
               time.sleep(ST)
           return True
               
   def irc_conn(self,n,u,r):
       self.nick(n)
       self.user(u,r)
       self.ping_pong()

                    
            #Commands...
       
   def connect(self,addr):
    try:
      self.samd=SAM().create_dest()
      #with SAM().create_dest() as dest:
      print("Connect to %s" % (addr) )
      self.sock=self.samd.connect(addr) 
      print("Connected to %s" % (addr) )
      return True
    except Exception as err:
      print ("Error %s" % err)
      self.sock.close()
      self.connect(addr)
   def __init__(self,dest,nick,username,realname):
        self.connect(dest)
        self.irc_conn(nick,username,realname)
        self.hand=handler(self.sock)
   def __del__(self):
       self.sock.close()
       pass
