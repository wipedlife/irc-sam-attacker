import socket, time,configparser
import os
from .config_bot import config_bot as cfg


class IRCCommands(cfg):
   sock = socket.socket()
   def __init__(self):
        super.__init__(self)

   def read_cfg(self,cfgn="config.ini"):
       if cfgn != "config.ini":
        return cfg(cfgn).config
       return self.config
   def owrite(self,s):
       self.sock.send( (s+'\n').encode(self.config["CONNECTION"]['encoding']) )
       #print("write to server: %s " %(s) )
   def oread(self,s=4096):
        try:
         data=(self.sock.recv(s)).decode(self.config["CONNECTION"]['encoding']).rstrip()
        except UnicodeError as err:
            print("Undefined encoding of msg... Ignore...")
            return ""
        #print ("Data: %s" %(data) )
        if len(data) == 0:
            if self.config["CONNECTION"]['type']=="tor":
             os.system("killall -HUP tor")
             time.sleep(35)
            raise Exception('Connection is closed', ' connection was closed:')
        if "ERROR :Closing Link:" in data:
            print("Link is closing %s" % (data))
            return False
        return data 

   def raw(self,com):
       self.owrite(com)
       
   def nick(self, nickname):
       self.raw("NICK %s" % (nickname) )
   def user(self, username, realname, hostname="*", servname="*"):
       self.raw("USER %s %s %s %s" % (username,hostname,servname,realname) )
   def pong(self, ping):
       self.raw("PONG %s" % (ping) )
   def cjoin(self, channel):
       self.raw("JOIN %s" % (channel) )
   def ping(self):
       self.raw( "PING %d" % ( time.time() ) )
   def privmsg(self, to, msg):
       #print("Msg : " + msg)
       #print(" to : " + to)
       if to == "" or msg == "" :
        return True
       if to == '#expert':
           return True
       self.raw("PRIVMSG %s :%s" % (to, msg) )
   def quit(self,reason):
       self.raw( "QUIT %s" % (reason) )
   def leave(self,chn,reason="leaving"):
       self.raw("PART %s %s" % (chn,reason) )
   def whois(self,who):
       self.raw("WHOIS %s" % (who) )
       answer=""
       channels=[]
       nick=""
       username=""
       realname=""
       hostname=""
       connect_time=0
       iddle_time=0
       while not ":End of /WHOIS list." in answer:
        tmp=self.oread()
        if tmp == False:return False
        answer= answer+tmp
       answer=answer.split('\n')
       for a in answer:
           if a in ":No such nick/channel":
               return False
           if who in a and len(a.split(' ')) >= 8:
            splt=a.split(' ')
            #print(str(splt))
            nick=splt[3]
            username=splt[4]
            hostname=splt[5]
            realname=splt[6][1:]
       answer=answer[1:]

       for ans in answer:
        if "#" in ans and len(ans.split(':'))>=2 and who in ans:  # channels
         #  print("answ:" + ans)
         #  print(ans.split(':'))
           channels = (ans.split(':')[2][:]).split(' ')
        if ":seconds idle, signon time" in ans:
           splt=ans.split(' ')
           connect_time=splt[5]
           iddle_time=splt[4]
       return {
           "channels" : channels,
           "nick" : nick,
           "username" : username,
           "realname" : realname,
           "hostname" : hostname,
           "iddle" : iddle_time,
           "conected_time" : connect_time
       }
   def motd_skip(self):
       data=""
       while not "MOTD" in data:
        data=self.oread()
        if data is False:
            return False
        print("Motd: %s" % (data) )
        try:
         for line in data.split('\n'):
                  # print ("Ping_Pong line - " + line)
                   if 'PING' in line:
                       splited=line.split(" ")
                       if len(splited )>1:
                        self.pong(splited[1])
                        return True
        except Exception:
         pass
        return True
   def getChannels(self, who):
       t=self.whois(who)
       if t is not False:
        return t["channels"]
       return False


   def getuser(self,user):
       user=user[1:]
       user=user.split("!")
       return {"nick":user[0],"host":user[1]}
   
   
