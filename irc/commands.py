import socket, time,configparser



class IRCCommands:
   sock=socket.socket()
   def read_cfg(self, cfg="config.ini"):
       c = configparser.ConfigParser()
       c.read(cfg)
       return c
   def owrite(self,s):
       self.sock.send( (s+'\n').encode() )
      # print("write to server: %s " %(s) )
   def oread(self,s=4096):
        data=(self.sock.recv(s)).decode().rstrip()
        #print ("Data: %s" %(data) )
        if len(data) == 0:
            raise Exception('Connection is closed', ' connection was closed:') 
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
        answer= answer+self.oread()
       answer=answer.split('\n')
       for a in answer:
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
       while not "MOTD" in self.oread():
        pass
   def getChannels(self, who):
       return self.whois(who)["channels"]



   def getuser(self,user):
       user=user[1:]
       user=user.split("!")
       return {"nick":user[0],"host":user[1]}
   
   
