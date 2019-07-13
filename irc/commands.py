import socket, time
class IRCCommands:
   sock=socket.socket()

   def owrite(self,s):
       self.sock.send( (s+'\n').encode() )
      # print("write to server: %s " %(s) )
   def oread(self,s=4096):
        data=(self.sock.recv(s)).decode()  
        #print ("Data: %s" %(data) )
        if len(data) == 0:
            raise Exception('Connection is closed', ' connection was closed') 
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
       
   def getuser(self,user):
       user=user[1:]
       user=user.split("!")
       return {"nick":user[0],"host":user[1]}
   
   
