from .commands import IRCCommands
from .handler_msg import handler_msg as handler
from leaflet import Controller as SAM
import socket,socks,random
import time,configparser
proxy_file="openproxy_list.txt"

class IRCOverlay(IRCCommands):
   samd=None           
   hand=None

   bot_dest=""
   bot_port = 0
   bot_nick=""
   bot_username=""
   bot_realname=""
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
       config = configparser.ConfigParser()
       config.read("config.ini")
       config = config["CONNECTION"]
       if config['ignore_ping'] != 'true':
        self.ping_pong()
       print("Motd skiping")
       if not self.motd_skip():
           print("Connection is was closed, try reconnect")
           time.sleep(15)
           self.__init__(self.bot_dest,self.bot_nick,self.bot_username,self.bot_realname,
                         p=self.bot_port)

       
                    
            #Commands...
       
   def connect(self,addr,typ="",port=6667):
     conf=  self.read_cfg("config.ini")
     torport=9050
     try:
      if not conf['CONNECTION']['type'] is None:
         typ=conf['CONNECTION']['type']
      if not conf['CONNECTION']['tor_port'] is None:
         torport=int(conf['CONNECTION']['tor_port'])
     except Exception:
         pass
     #print("Connect with type: "+str(typ))
     try:
       if "i2p" in typ:
          self.samd=SAM().create_dest()
          #with SAM().create_dest() as dest:
          print("Connect to %s" % (addr) )
          self.sock=self.samd.connect(addr)
          answer=self.oread()
          if "RESULT=OK" in answer:
           print("Connected to %s" % (addr) )
           return True
          else:
           print("Can't connect to %s" % (addr) )
           raise Exception("Can't connect to server", "Error with connect:  %s" % (answer) )
       elif "clear" in typ or "tor" in typ or "openproxy":
           if "tor" in typ or "openproxy" in typ:
               if typ == "tor":
                  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', torport, True)
               elif typ == "openproxy":
                   with open(proxy_file,"r+") as openproxy:

                       list_openproxy=openproxy.read().split('\n')
                       success=False
                       while not success:
                        try:
                         proxy=list_openproxy[random.randrange(0,len(list_openproxy)-1)].split(':')
                         proxy[1]=int(proxy[1])
                         print("Connect to %s:%d" % (proxy[0], proxy[1]))
                         socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy[0], int(proxy[1]), True)
                         print("Connected to %s:%d" % (proxy[0],proxy[1]))
                         success=True
                        except Exception:
                            print("cant connect to %s:%d" % (proxy[0],proxy[1]))
                            success=False
                            continue

                   pass
               self.sock=socks.socksocket()
           else:
            self.sock=socket.socket()


           self.sock.connect((addr,port))
       else:
           raise Exception("undefined type", "Undefined type of connection")
     except OSError as msg:
           self.sock.close()
           raise Exception ('Cant connect',"Can't connest to %s : %d" % (addr, port))
   def __init__(self,dest,nick,username,realname,p=6667):
       self.bot_dest = dest
       self.bot_port = p
       self.bot_nick = nick
       self.bot_username = username
       self.bot_realname = realname

       if dest is None:
          self.sock.close()
          return None
       self.connect(dest,port=p)
       self.irc_conn(nick,username,realname)
       self.hand=handler(self.sock)

   def __del__(self):
       self.sock.close()
       pass
